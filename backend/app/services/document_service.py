import os
import shutil

from fastapi import UploadFile

from app.rag.pdf_reader import load_pdf
from app.rag.text_splitter import split_documents
from app.rag.vector_store import create_vector_store

DOCUMENT_FOLDER = "documents"

os.makedirs(DOCUMENT_FOLDER, exist_ok=True)


def save_document(file: UploadFile):

    file_path = os.path.join(DOCUMENT_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    documents = load_pdf(file_path)

    chunks = split_documents(documents)

    vector_store = create_vector_store(chunks, file.filename)

    return file_path, documents, chunks