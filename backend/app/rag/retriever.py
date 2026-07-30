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

    filter_dict = None
    if selected_document:
        filter_dict = {"source": selected_document}

    return vector_store.max_marginal_relevance_search(
        question,
        k=4,
        fetch_k=10,
        filter=filter_dict
    )