from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.conversation import Conversation


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


class ConversationCreate(BaseModel):
    title: str
    document_id: int | None = None


@router.post("/")
def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db)
):
    conversation = Conversation(
        title=request.title,
        document_id=request.document_id
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "id": conversation.id,
        "title": conversation.title,
        "document_id": conversation.document_id,
        "created_at": conversation.created_at
    }