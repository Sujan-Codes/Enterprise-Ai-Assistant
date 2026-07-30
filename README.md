# Enterprise AI Assistant

A full-stack, locally-running AI assistant that lets you upload PDF documents and have intelligent conversations with them — powered by **Ollama (Llama 3.2)**, **FAISS vector search**, and **RAG (Retrieval-Augmented Generation)**.

---

## Features

- 📄 **PDF Upload & Indexing** — Upload any PDF; it is chunked, embedded, and stored in a FAISS vector index
- 🔍 **RAG Pipeline** — Questions are answered strictly from the uploaded document context
- 📂 **Document Selection** — Click a document in the sidebar to scope retrieval to that file only, preventing cross-document mixing
- 💬 **Multi-Chat Sessions** — Each conversation is isolated with its own history and active document
- ⚡ **Streaming Responses** — Answers stream token-by-token via Server-Sent Events (SSE)
- 🕐 **Timestamps** — Every message shows the time it was sent
- 🟢 **System Status Card** — Live sidebar indicator showing Ollama connectivity, FAISS index state, and loaded model
- 🧠 **Conversation Memory** — Follow-up questions are rewritten as standalone queries using chat history
- 🐳 **Docker Support** — One-command startup with `docker-compose`

---

## Tech Stack

| Layer     | Technology                                      |
|-----------|-------------------------------------------------|
| Frontend  | React 18, Vite, react-markdown                  |
| Backend   | FastAPI, Python 3.11+                           |
| LLM       | Ollama — Llama 3.2 (runs locally)               |
| Embeddings| sentence-transformers/all-MiniLM-L6-v2          |
| Vector DB | FAISS (local, persistent)                       |
| PDF Parse | LangChain PyPDFLoader                           |
| Container | Docker + Docker Compose                         |

---

## Project Structure

```
enterprise-ai-assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py          # /chat/ and /chat/stream endpoints
│   │   │   └── upload.py        # /documents/upload and /documents/
│   │   ├── rag/
│   │   │   ├── pdf_reader.py    # PDF loading
│   │   │   ├── text_splitter.py # Chunk splitting
│   │   │   ├── retriever.py     # FAISS search with optional doc filter
│   │   │   └── vector_store.py  # FAISS index (merge on upload)
│   │   ├── services/
│   │   │   ├── llm_service.py   # rewrite_query, generate_answer, stream_answer
│   │   │   └── document_service.py
│   │   └── main.py              # FastAPI app + /status endpoint
│   ├── documents/               # Uploaded PDFs stored here
│   ├── faiss_index/             # Persisted FAISS index (git-ignored)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx      # Chat list, doc selector, status card
│   │   │   ├── ChatWindow.jsx   # Message rendering with timestamps
│   │   │   ├── ChatInput.jsx    # SSE streaming input
│   │   │   └── UploadDocument.jsx
│   │   ├── pages/
│   │   │   ├── Chat.jsx         # Multi-chat state management
│   │   │   └── Login.jsx
│   │   ├── services/api.js
│   │   └── styles.css
│   └── package.json
└── docker-compose.yml
```

---

## Getting Started

### Prerequisites

- [Ollama](https://ollama.com) installed and running
- Llama 3.2 pulled: `ollama pull llama3.2`
- Docker & Docker Compose (for containerised setup)
- Node.js 18+ and Python 3.11+ (for local dev)

### Option 1 — Docker (recommended)

```bash
git clone https://github.com/Sujan-Codes/Enterprise-Ai-Assistant.git
cd Enterprise-Ai-Assistant
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2 — Local Development

**Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

---

## How It Works

```
User uploads PDF
      ↓
PyPDFLoader → text chunks → HuggingFace embeddings → FAISS index (merged, persistent)

User selects a document + asks a question
      ↓
Query rewritten (if follow-up) → FAISS filtered search (selected doc only)
      ↓
Top-k chunks → Llama 3.2 prompt → streamed SSE response → React renders token-by-token
```

---

## API Endpoints

| Method | Endpoint            | Description                        |
|--------|---------------------|------------------------------------|
| GET    | `/status`           | Ollama, FAISS, and doc health check|
| GET    | `/documents/`       | List uploaded PDFs                 |
| POST   | `/documents/upload` | Upload and index a PDF             |
| POST   | `/chat/`            | Single-shot Q&A                    |
| POST   | `/chat/stream`      | Streaming SSE Q&A                  |

---

## Environment

Create `backend/.env` for any overrides:

```env
# No secrets required for local Ollama setup
```

---

## License

MIT
