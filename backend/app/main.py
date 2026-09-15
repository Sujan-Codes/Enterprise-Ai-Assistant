import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.conversation import router as conversation_router
from app.api.message import router as message_router
from app.models.document import Document
from app.models.conversation import Conversation
from app.models.message import Message


app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(conversation_router)
app.include_router(message_router)

@app.get("/status")
def status():
    import requests as req
    # Check Ollama
    try:
        r = req.get("http://localhost:11434/api/tags", timeout=2)
        models = [m["name"] for m in r.json().get("models", [])]
        ollama_ok = True
    except Exception:
        models = []
        ollama_ok = False

    faiss_ok = os.path.exists("faiss_indexes") and any(
        os.path.isdir(os.path.join("faiss_indexes", d))
        for d in os.listdir("faiss_indexes")
    ) if os.path.exists("faiss_indexes") else False

    doc_count = 0
    if os.path.exists("documents"):
        doc_count = len([f for f in os.listdir("documents") if f.lower().endswith(".pdf")])

    return {
        "ollama": ollama_ok,
        "faiss": faiss_ok,
        "doc_count": doc_count,
        "models": models,
    }