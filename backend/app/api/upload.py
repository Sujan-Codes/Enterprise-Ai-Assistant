import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_service import save_document

DOCUMENTS_DIR = "documents"

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("/")
def list_documents():
    if not os.path.exists(DOCUMENTS_DIR):
        return []
    return [
        f for f in os.listdir(DOCUMENTS_DIR)
        if f.lower().endswith(".pdf")
    ]


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path, documents, chunks = save_document(file)

    return {
        "message": "Document uploaded successfully",
        "filename": file.filename,
        "pages": len(documents),
        "chunks_created": len(chunks),
        "first_chunk": chunks[0].page_content[:300]
    }