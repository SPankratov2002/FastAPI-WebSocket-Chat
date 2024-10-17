import React, { useState, useEffect, useRef } from "react";

function Chat({ username, token }) {
  // Стейт для отслеживания текущего сообщения и всех полученных сообщений
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  // Используем useRef для хранения экземпляра WebSocket, чтобы избежать пересоздания
  const socketRef = useRef(null);

  // useEffect для инициализации WebSocket-соединения при изменении токена или имени пользователя
  useEffect(() => {
    if (token && username) {
      const ws = new WebSocket(
        `ws://127.0.0.1:8000/ws/chat/${username}?token=${token}`
      );
      socketRef.current = ws; // Сохраняем WebSocket-соединение в ref

      // Событие при успешном подключении к WebSocket
      ws.onopen = () => {
        console.log("Connected to WebSocket");
      };

      // Событие при получении сообщения: обновляем список сообщений
      ws.onmessage = (event) => {
        setMessages((prevMessages) => [...prevMessages, event.data]);
      };

      // Событие при закрытии WebSocket-соединения
      ws.onclose = () => {
        console.log("Disconnected from WebSocket");
      };

      // Очистка: закрываем WebSocket при размонтировании компонента
      return () => {
        ws.close();
      };
    }
  }, [token, username]); // Запускаем эффект только при изменении token или username

  // Функция для отправки сообщения через WebSocket
  const sendMessage = () => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(message); // Отправляем сообщение через WebSocket
      setMessage(""); // Очищаем поле ввода после отправки
    } else {
      console.log("WebSocket is not open");
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="text-left mb-4">Chat</h2>
      <div
        className="chat-box mb-4 p-3 border rounded bg-light"
        style={{ height: "300px", overflowY: "scroll" }}
      >
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <div key={index} className="mb-2">
              {msg}
            </div>
          ))
        ) : (
          <p className="text-muted">No messages yet...</p>
        )}
      </div>

      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Enter your message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button className="btn btn-primary" onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;
