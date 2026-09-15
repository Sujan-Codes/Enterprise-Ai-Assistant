from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.message import Message
from app.models.conversation import Conversation


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


class MessageCreate(BaseModel):
    conversation_id: int
    role: str
    content: str


@router.post("/")
def create_message(
    request: MessageCreate,
    db: Session = Depends(get_db)
):

    # Check whether conversation exists
    conversation = db.get(
        Conversation,
        request.conversation_id
    )

    if not conversation:
        return {
            "error": "Conversation not found"
        }

    # Create message
    message = Message(
        conversation_id=request.conversation_id,
        role=request.role,
        content=request.content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "role": message.role,
        "content": message.content,
        "created_at": message.created_at
    }