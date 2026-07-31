import { useState, useCallback } from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import api from "../services/api";

let nextId = 1;
const newChat = (title = "New Chat", attachedDoc = null) => ({
  id: nextId++,
  title,
  attachedDoc,
  messages: [],
});

function Chat() {
  const [chats, setChats] = useState([newChat()]);
  const [activeChatId, setActiveChatId] = useState(1);

  const activeChat = chats.find((c) => c.id === activeChatId);

  const updateChat = useCallback((id, patch) => {
    setChats((prev) => prev.map((c) => (c.id === id ? { ...c, ...patch } : c)));
  }, []);

  const handleNewChat = () => {
    const chat = newChat();
    setChats((prev) => [...prev, chat]);
    setActiveChatId(chat.id);
  };

  const handleUpload = async (file) => {
    if (!file) return null;
    const formData = new FormData();
    formData.append("file", file);
    const res = await api.post("/documents/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data.filename;
  };

  const handleAttach = async (file) => {
    const filename = await handleUpload(file);
    if (!filename) return;
    const title = filename.replace(/\.pdf$/i, "");
    const chat = newChat(title, filename);
    setChats((prev) => [...prev, chat]);
    setActiveChatId(chat.id);
    return filename;
  };

  return (
    <div className="container">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onSelectChat={setActiveChatId}
        onNewChat={handleNewChat}
      />
      <div className="chat-section">
        <ChatWindow messages={activeChat.messages} attachedDoc={activeChat.attachedDoc} />
        <ChatInput
          chatId={activeChatId}
          messages={activeChat.messages}
          selectedDoc={activeChat.attachedDoc}
          onAttach={handleAttach}
          onUpdate={(messages, title) =>
            updateChat(activeChatId, title ? { messages, title } : { messages })
          }
        />
      </div>
    </div>
  );
}

export default Chat;
