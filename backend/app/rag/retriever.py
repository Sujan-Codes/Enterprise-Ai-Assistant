import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

INDEXES_DIR = "faiss_indexes"


def search_documents(question: str, selected_document: str = None):
    if selected_document:
        index_path = os.path.join(INDEXES_DIR, selected_document.replace(".pdf", ""))
        if not os.path.exists(index_path):
            return []
        vector_store = FAISS.load_local(
            index_path, embeddings, allow_dangerous_deserialization=True
        )
        return vector_store.max_marginal_relevance_search(question, k=6, fetch_k=20)

    # No document selected — search across all available indexes
    if not os.path.exists(INDEXES_DIR):
        return []

    all_docs = []
    for name in os.listdir(INDEXES_DIR):
        index_path = os.path.join(INDEXES_DIR, name)
        if not os.path.isdir(index_path):
            continue
        try:
            vs = FAISS.load_local(
                index_path, embeddings, allow_dangerous_deserialization=True
            )
            all_docs.extend(vs.max_marginal_relevance_search(question, k=2, fetch_k=10))
        except Exception:
            continue

    return all_docs
