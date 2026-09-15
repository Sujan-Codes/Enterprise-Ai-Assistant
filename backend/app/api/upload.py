import os

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.document_service import save_document
from app.database import get_db
from app.models.document import Document


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
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path, documents, chunks, safe_name = save_document(file)

    # Create database record
    document = Document(
        filename=safe_name,
        file_path=file_path
    )

    # Add record to database
    db.add(document)

    # Save changes permanently
    db.commit()

    # Get generated ID
    db.refresh(document)

    return {
        "message": "Document uploaded successfully",
        "document_id": document.id,
        "filename": safe_name,
        "pages": len(documents),
        "chunks_created": len(chunks),
        "first_chunk": chunks[0].page_content[:300]
    }