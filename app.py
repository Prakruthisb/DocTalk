from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from src.document_loader import load_and_chunk
from src.vector_store import build_vector_store, get_retriever
from src.rag_chain import build_rag_chain, ask
from src.multilingual import detect_and_translate_to_english, translate_answer
import tempfile

st.set_page_config(page_title="DocTalk", layout="centered")
st.title("DocTalk — Chat with any document in your language")

# ── 1. Initialise session state ──────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []      # chat history for display

if "chain" not in st.session_state:
    st.session_state.chain = None       # RAG chain persists across reruns

if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False

# ── 2. File upload ───────────────────────────────────────────
uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded and not st.session_state.doc_loaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(uploaded.read())
        tmp_path = f.name

    with st.spinner("Processing document..."):
        chunks = load_and_chunk(tmp_path)
        vs = build_vector_store(chunks)
        retriever = get_retriever(vs)
        st.session_state.chain = build_rag_chain(retriever)
        st.session_state.doc_loaded = True
    st.success(f"Ready — {len(chunks)} chunks indexed")

# ── 3. Render existing chat history ─────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 4. Chat input ────────────────────────────────────────────
if st.session_state.doc_loaded:
    question = st.text_input("Ask a question (any Indian language or English)")

    if question:
        # Show user message immediately
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                eng_q, detected = detect_and_translate_to_english(question)
                answer, sources = ask(st.session_state.chain, eng_q)
                final_answer = translate_answer(answer, detected)

            st.write(final_answer)

            if sources:
                # Deduplicate pages — same page can appear multiple times
                seen_pages = []
                unique_sources = []
                for doc in sources:
                    page = doc.metadata.get('page', 'Unknown')
                    if page not in seen_pages:
                        seen_pages.append(page)
                        unique_sources.append(doc)

                # Clean page label
                page_labels = [f"Page {p + 1}" for p in seen_pages]  # +1 because pages are 0-indexed
                st.caption(f"📄 Answer found on: {', '.join(page_labels)}")

                with st.expander("View source excerpts"):
                    for doc in unique_sources:
                        page_num = doc.metadata.get('page', 0) + 1
                        st.markdown(f"**Page {page_num}**")
                        st.text(doc.page_content[:400] + "...")
                        st.divider()

        # Save assistant message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": final_answer
        })
else:
    st.info("Upload a PDF above to start chatting")

with st.sidebar:
    st.header("DocTalk")
    if st.button("Clear chat history"):
        st.session_state.messages = []
        st.session_state.chain = None
        st.session_state.doc_loaded = False
        st.rerun()