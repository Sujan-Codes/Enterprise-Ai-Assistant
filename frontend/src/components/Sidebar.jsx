import { useState, useEffect } from "react";
import UploadDocument from "./UploadDocument";
import api from "../services/api";

function StatusCard() {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    api.get("/status").then((r) => setStatus(r.data)).catch(() => setStatus(null));
  }, []);

  if (!status) return null;

  const dot = (ok) => (
    <span style={{ color: ok ? "#22c55e" : "#ef4444" }}>{ok ? "🟢" : "🔴"}</span>
  );

  return (
    <div className="status-card">
      <div className="status-row">{dot(status.ollama)} Ollama</div>
      <div className="status-row">{dot(status.faiss)} FAISS Index</div>
      <div className="status-row">{dot(status.doc_count > 0)} {status.doc_count} doc{status.doc_count !== 1 ? "s" : ""} indexed</div>
      {status.models[0] && (
        <div className="status-row" style={{ color: "#64748b", fontSize: 11 }}>
          ⚙ {status.models[0]}
        </div>
      )}
    </div>
  );
}

function Sidebar({ chats, activeChatId, onSelectChat, onNewChat, selectedDoc, setSelectedDoc }) {
  const [docs, setDocs] = useState([]);

  const fetchDocs = () => {
    api.get("/documents").then((r) => setDocs(r.data)).catch(() => {});
  };

  useEffect(() => { fetchDocs(); }, []);

  return (
    <div className="sidebar">
      <h2>Enterprise AI</h2>

      <button className="new-chat-btn" onClick={onNewChat}>+ New Chat</button>

      <div className="chat-list">
        {chats.map((c) => (
          <div
            key={c.id}
            className={`chat-item ${c.id === activeChatId ? "chat-item-active" : ""}`}
            onClick={() => onSelectChat(c.id)}
          >
            💬 {c.title}
          </div>
        ))}
      </div>

      <hr />

      <UploadDocument onUpload={fetchDocs} />

      <h3>Uploaded Documents</h3>
      <ul className="doc-list">
        {docs.map((name, i) => (
          <li
            key={i}
            className={`doc-item ${selectedDoc === name ? "doc-active" : ""}`}
            onClick={() => setSelectedDoc(selectedDoc === name ? null : name)}
          >
            <span>{selectedDoc === name ? "📂" : "📄"}</span>
            <span className="doc-name">{name}</span>
            {selectedDoc === name && <span className="doc-badge">Active</span>}
          </li>
        ))}
      </ul>
      {selectedDoc && (
        <button className="clear-selection" onClick={() => setSelectedDoc(null)}>
          ✕ Clear selection
        </button>
      )}

      <div style={{ flex: 1 }} />
      <StatusCard />
    </div>
  );
}

export default Sidebar;
