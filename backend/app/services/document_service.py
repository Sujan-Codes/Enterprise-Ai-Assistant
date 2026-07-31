import os
import shutil
from pathlib import Path

from fastapi import UploadFile
from werkzeug.utils import secure_filename

from app.rag.pdf_reader import load_pdf
from app.rag.text_splitter import split_documents
from app.rag.vector_store import create_vector_store

DOCUMENT_FOLDER = "documents"

os.makedirs(DOCUMENT_FOLDER, exist_ok=True)


def save_document(file: UploadFile):
    safe_name = secure_filename(file.filename)
    if not safe_name:
        raise ValueError("Invalid filename")

    file_path = str(Path(DOCUMENT_FOLDER) / safe_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    documents = load_pdf(file_path)
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks, safe_name)

    return file_path, documents, chunks, safe_name