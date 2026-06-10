from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from src.document_loader import load_and_chunk
from src.vector_store import build_vector_store, get_retriever
from src.rag_chain import build_rag_chain, ask
from src.multilingual import detect_and_translate_to_english, translate_answer
import tempfile, os

st.set_page_config(page_title="DocTalk", layout="centered")
st.title("DocTalk — Chat with any document in your language")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(uploaded.read())
        tmp_path = f.name

    with st.spinner("Processing document..."):
        chunks = load_and_chunk(tmp_path)
        vs = build_vector_store(chunks)
        retriever = get_retriever(vs)
        chain = build_rag_chain(retriever)
    st.success(f"Ready — {len(chunks)} chunks indexed")

    question = st.text_input("Ask a question (any Indian language or English)")

    if question:
        with st.spinner("Thinking..."):
            eng_q, detected = detect_and_translate_to_english(question)
            answer, sources = ask(chain, eng_q)
            final_answer = translate_answer(answer, detected)

        st.markdown("### Answer")
        st.write(final_answer)

        with st.expander("Source chunks used"):
            for doc in sources:
                st.caption(f"Page {doc.metadata.get('page', '?')}")
                st.text(doc.page_content[:300] + "...")