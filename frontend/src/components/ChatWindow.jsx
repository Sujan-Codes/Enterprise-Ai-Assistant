import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

function formatTime(date) {
  if (!date) return "";
  const d = date instanceof Date ? date : new Date(date);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function ChatWindow({ messages, attachedDoc }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-window">
      {attachedDoc && (
        <div className="chat-doc-header">
          📄 {attachedDoc}
        </div>
      )}

      {messages.length === 0 && (
        <div className="bubble ai">
          <span className="bubble-avatar">🤖</span>
          <div className="bubble-content">
            {attachedDoc
              ? "Ask me anything about this document."
              : "Hello 👋 Upload a PDF to get started."}
          </div>
        </div>
      )}

      {messages.map((msg, i) => {
        const isStreaming = msg.type === "ai" && msg.text === "" && i === messages.length - 1;
        return (
          <div key={i} className={`bubble ${msg.type}`}>
            {msg.type === "ai" && <span className="bubble-avatar">🤖</span>}
            <div className="bubble-content">
              {isStreaming ? (
                <div className="typing"><span /><span /><span /></div>
              ) : (
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              )}
              {msg.sources?.length > 0 && (
                <div className="sources">
                  {msg.sources.map((s, j) => {
                    const fileName = s.source.split("\\").pop().split("/").pop();
                    return (
                      <small key={j}>📄 {fileName} • Page {s.page + 1}</small>
                    );
                  })}
                </div>
              )}
              {msg.time && (
                <div className="msg-time">{formatTime(msg.time)}</div>
              )}
            </div>
          </div>
        );
      })}

      <div ref={bottomRef} />
    </div>
  );
}

export default ChatWindow;
