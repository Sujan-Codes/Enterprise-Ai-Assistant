import { useState, useRef } from "react";

function ChatInput({ messages, selectedDoc, onAttach, onUpdate }) {
  const [question, setQuestion] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const activeDoc = selectedDoc;

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    e.target.value = "";
    if (!file) return;
    setUploading(true);
    try {
      await onAttach(file);
    } catch {
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim() || streaming) return;

    const userMsg = { type: "user", text: question, time: new Date() };
    const aiMsg = { type: "ai", text: "", sources: [], time: new Date() };
    const nextMessages = [...messages, userMsg, aiMsg];

    const isFirstMessage = messages.length === 0;
    onUpdate(nextMessages, isFirstMessage ? question.slice(0, 40) : undefined);
    setQuestion("");
    setStreaming(true);

    const history = messages.map((m) => ({
      role: m.type === "user" ? "user" : "assistant",
      content: m.text,
    }));

    try {
      const res = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, history, selected_document: activeDoc || undefined }),
      });

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let accumulated = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter((l) => l.startsWith("data: "));

        for (const line of lines) {
          const data = JSON.parse(line.slice(6));
          if (data.token !== undefined) {
            accumulated += data.token;
            onUpdate(
              nextMessages.map((m, i) =>
                i === nextMessages.length - 1 ? { ...m, text: accumulated } : m
              )
            );
          } else if (data.done) {
            onUpdate(
              nextMessages.map((m, i) =>
                i === nextMessages.length - 1
                  ? { ...m, text: accumulated, sources: data.sources }
                  : m
              )
            );
          }
        }
      }
    } catch {
      onUpdate(
        nextMessages.map((m, i) =>
          i === nextMessages.length - 1
            ? { ...m, text: "⚠️ Unable to get a response. Please try again." }
            : m
        )
      );
    } finally {
      setStreaming(false);
    }
  };

  return (
    <div className="input-area">
      {activeDoc && (
        <div className="attachment-chip">
          <span>📄 {activeDoc}</span>
  
        </div>
      )}

      <div className="chat-input">
        <button
          className="attach-btn"
          onClick={() => fileInputRef.current?.click()}
          disabled={streaming || uploading}
          title="Attach PDF"
        >
          {uploading ? "⏳" : "+"}
        </button>
        <input
          type="file"
          accept=".pdf"
          ref={fileInputRef}
          onChange={handleFileChange}
          hidden
        />
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={activeDoc ? `Ask about ${activeDoc}…` : "Ask anything or attach a PDF…"}
          onKeyDown={(e) => { if (e.key === "Enter") askQuestion(); }}
          disabled={streaming}
        />
        <button onClick={askQuestion} disabled={streaming || !question.trim()}>
          {streaming ? "…" : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatInput;
