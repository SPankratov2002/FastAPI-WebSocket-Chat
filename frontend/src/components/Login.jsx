import React, { useState } from "react";

function Login({ onLogin }) {
  // Стейты для имени пользователя, пароля и сообщения (например, об ошибке)
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  // Обработка логина пользователя
  const handleLogin = async () => {
    // Отправляем POST-запрос на сервер для получения токена
    const response = await fetch("http://127.0.0.1:8000/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: username,
        password: password,
      }),
    });

    const data = await response.json();

    // Проверяем успешность запроса и обрабатываем результат
    if (response.ok) {
      setMessage("Login successful!");
      // Передаем токен и имя пользователя родительскому компоненту
      onLogin(data.access_token, username);
    } else {
      setMessage(data.detail || "Login failed"); // Показываем сообщение об ошибке
    }
  };

  return (
    <div className="container d-flex flex-column justify-content-center align-items-center">
      <div className="card p-4" style={{ width: "400px", height: "400px" }}>
        <h2 className="text-center mb-4">Login</h2>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">
            Username
          </label>
          <input
            type="text"
            className="form-control"
            id="username"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            type="password"
            className="form-control"
            id="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button onClick={handleLogin} className="btn btn-primary w-100 mt-auto">
          Login
        </button>
        {message && <p className="mt-3 text-center">{message}</p>}
      </div>
    </div>
  );
}

export default Login;
