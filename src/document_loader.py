import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_loader(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        return PyMuPDFLoader(file_path)
    elif ext == ".txt":
        return TextLoader(file_path, encoding="utf-8")
    elif ext == ".docx":
        return Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def load_and_chunk(file_path):
    loader = get_loader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks