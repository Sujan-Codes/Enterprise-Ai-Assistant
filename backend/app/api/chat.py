import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message

from app.rag.retriever import search_documents
from app.services.llm_service import (
    generate_answer,
    rewrite_query,
    stream_answer
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str

    history: Optional[List[HistoryMessage]] = []

    selected_document: Optional[str] = None

    conversation_id: Optional[int] = None


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------
    # 1. Validate conversation
    # --------------------------------

    if not request.conversation_id:
        raise HTTPException(
            status_code=400,
            detail="conversation_id is required"
        )

    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    # --------------------------------
    # 2. Save USER message
    # --------------------------------

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.question
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)


    # --------------------------------
    # 3. Rewrite query if needed
    # --------------------------------

    query = request.question

    if request.history:
        query = rewrite_query(
            request.question,
            request.history
        )


    # --------------------------------
    # 4. Retrieve documents from FAISS
    # --------------------------------

    docs = search_documents(
        query,
        request.selected_document
    )


    # --------------------------------
    # 5. Generate AI answer
    # --------------------------------

    answer = generate_answer(
        request.question,
        docs,
        request.history
    )


    # --------------------------------
    # 6. Save AI message
    # --------------------------------

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=answer
    )

    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)


    # --------------------------------
    # 7. Prepare sources
    # --------------------------------

    unique_sources = []

    seen = set()

    for doc in docs:

        source = doc.metadata.get("source")
        page = doc.metadata.get("page")

        key = (source, page)

        if key not in seen:

            seen.add(key)

            unique_sources.append({
                "page": page,
                "source": source
            })


    # --------------------------------
    # 8. Return response
    # --------------------------------

    return {
        "question": request.question,
        "answer": answer,
        "conversation_id": conversation.id,
        "message_id": assistant_message.id,
        "sources": unique_sources
    }