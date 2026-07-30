from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path: str):
    """
    Reads a PDF and returns its pages as LangChain Documents.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents