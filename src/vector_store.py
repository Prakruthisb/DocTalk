from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_vector_store(chunks):
    # Same sentence-transformers you used in Movie Recommender
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    # Build FAISS index from chunks
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def get_retriever(vector_store, k=4):
    # k = number of chunks to retrieve per query
    return vector_store.as_retriever(
        search_kwargs={"k": k}
    )