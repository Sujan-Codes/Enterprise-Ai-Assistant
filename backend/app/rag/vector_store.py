import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

INDEXES_DIR = "faiss_indexes"


def _safe_folder_name(doc_name: str) -> str:
    name = doc_name.replace(".pdf", "").replace(".PDF", "")
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)


def create_vector_store(chunks, doc_name: str):
    index_path = os.path.join(INDEXES_DIR, _safe_folder_name(doc_name))
    os.makedirs(index_path, exist_ok=True)
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(index_path)
    return vector_store
