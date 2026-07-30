import { useState, useCallback } from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

let nextId = 1;
const newChat = () => ({ id: nextId++, title: "New Chat", messages: [], selectedDoc: null });

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

  return (
    <div className="container">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onSelectChat={setActiveChatId}
        onNewChat={handleNewChat}
        selectedDoc={activeChat.selectedDoc}
        setSelectedDoc={(doc) => updateChat(activeChatId, { selectedDoc: doc })}
      />
      <div className="chat-section">
        <ChatWindow messages={activeChat.messages} />
        <ChatInput
          chatId={activeChatId}
          messages={activeChat.messages}
          selectedDoc={activeChat.selectedDoc}
          onUpdate={(messages, title) =>
            updateChat(activeChatId, title ? { messages, title } : { messages })
          }
        />
      </div>
    </div>
  );
}

export default Chat;
