from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json

from app.rag.retriever import search_documents
from app.services.llm_service import generate_answer, rewrite_query, stream_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    history: Optional[List[HistoryMessage]] = []
    selected_document: Optional[str] = None


@router.post("/")
def chat(request: ChatRequest):
    query = rewrite_query(request.question, request.history) if request.history else request.question
    docs = search_documents(query, request.selected_document)
    answer = generate_answer(query, docs, request.history)

    unique_sources = []
    seen = set()
    for doc in docs:
        source = doc.metadata.get("source")
        page = doc.metadata.get("page")
        key = (source, page)
        if key not in seen:
            seen.add(key)
            unique_sources.append({"page": page, "source": source})

    return {"question": request.question, "answer": answer, "sources": unique_sources}


@router.post("/stream")
def chat_stream(request: ChatRequest):
    query = rewrite_query(request.question, request.history) if request.history else request.question
    docs = search_documents(query, request.selected_document)

    unique_sources = []
    seen = set()
    for doc in docs:
        source = doc.metadata.get("source")
        page = doc.metadata.get("page")
        key = (source, page)
        if key not in seen:
            seen.add(key)
            unique_sources.append({"page": page, "source": source})

    def event_stream():
        for token in stream_answer(query, docs, request.history):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield f"data: {json.dumps({'done': True, 'sources': unique_sources})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
