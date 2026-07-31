import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME
)

def search_documents(question: str, selected_document: str = None):

    if not os.path.exists("faiss_index"):
        return []

    vector_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = vector_store.max_marginal_relevance_search(question, k=4, fetch_k=20)

    if selected_document:
        docs = [
            doc for doc in docs
            if os.path.basename(doc.metadata.get("source", "")) == selected_document
        ]

    return docs