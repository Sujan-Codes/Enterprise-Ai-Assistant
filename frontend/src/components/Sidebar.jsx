import { useState, useEffect } from "react";
import api from "../services/api";
import ThemeToggle from "./ThemeToggle";

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
      <div className="status-row">
        {dot(status.doc_count > 0)} {status.doc_count} doc{status.doc_count !== 1 ? "s" : ""} indexed
      </div>
      {status.models[0] && (
        <div className="status-row" style={{ color: "#64748b", fontSize: 11 }}>
          ⚙ {status.models[0]}
        </div>
      )}
    </div>
  );
}

function Sidebar({ chats, activeChatId, onSelectChat, onNewChat }) {
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

      <div style={{ flex: 1 }} />
      <StatusCard />
      <ThemeToggle />
    </div>
  );
}

export default Sidebar;
