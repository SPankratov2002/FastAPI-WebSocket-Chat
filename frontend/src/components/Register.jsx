import React, { useState } from "react";

function Register() {
  // Стейты для управления значениями полей ввода и сообщения об ошибке/успехе
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  // Функция для обработки регистрации пользователя
  const handleRegister = async () => {
    // Отправляем POST-запрос на сервер для регистрации
    const response = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    });

    const data = await response.json();

    // Проверяем успешность запроса и обновляем сообщение
    if (response.ok) {
      setMessage("Registration successful!");
    } else {
      setMessage(data.detail || "Registration failed");
    }
  };

  return (
    <div className="container d-flex flex-column justify-content-center align-items-center">
      <div className="card p-4" style={{ width: "400px", height: "400px" }}>
        <h2 className="text-center mb-4">Register</h2>
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
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            type="email"
            className="form-control"
            id="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
        <button onClick={handleRegister} className="btn btn-primary w-100">
          Register
        </button>
        {message && <p className="mt-3 text-center">{message}</p>}
      </div>
    </div>
  );
}

export default Register;
