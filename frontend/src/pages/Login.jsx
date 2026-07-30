import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    // Placeholder auth — replace with real API call
    if (username && password) navigate("/chat");
  }

  return (
    <div style={{
      minHeight: "100vh", display: "flex", alignItems: "center",
      justifyContent: "center", background: "#020617",
    }}>
      <form onSubmit={handleSubmit} style={{
        background: "#0f172a", padding: 32, borderRadius: 12,
        display: "flex", flexDirection: "column", gap: 16, width: 320,
        border: "1px solid #1e293b",
      }}>
        <h1 style={{ color: "#f1f5f9", fontSize: 20, fontWeight: 700, margin: 0 }}>
          🤖 Enterprise AI
        </h1>
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={inputStyle}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={inputStyle}
        />
        <button type="submit" style={{
          padding: "10px", borderRadius: 8, border: "none",
          background: "#2563eb", color: "#fff", cursor: "pointer", fontSize: 14,
        }}>
          Sign In
        </button>
      </form>
    </div>
  );
}

const inputStyle = {
  padding: "10px 14px", borderRadius: 8, border: "1px solid #334155",
  background: "#020617", color: "#f1f5f9", fontSize: 14, outline: "none",
};
