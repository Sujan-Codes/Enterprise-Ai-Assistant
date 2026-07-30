export default function MessageBubble({ message }) {
  const isUser = message.role === "user";
  return (
    <div style={{ display: "flex", justifyContent: isUser ? "flex-end" : "flex-start", marginBottom: 12 }}>
      <div style={{
        maxWidth: "70%",
        padding: "10px 14px",
        borderRadius: 12,
        background: isUser ? "#2563eb" : "#1e293b",
        color: "#f1f5f9",
        fontSize: 14,
        lineHeight: 1.5,
      }}>
        {message.content}
        {message.sources?.length > 0 && (
          <div style={{ marginTop: 8, fontSize: 11, opacity: 0.6 }}>
            {message.sources.map((s, i) => (
              <div key={i}>📄 {s.source} — page {s.page}</div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
