from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk(pdf_path):
    # Load PDF — each page becomes a Document object
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    # Split into overlapping chunks
    # chunk_size: how many characters per chunk
    # chunk_overlap: overlap between chunks so context isn't lost
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks