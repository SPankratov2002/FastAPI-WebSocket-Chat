import React, { useState } from "react";
import Chat from "./components/Chat";
import Login from "./components/Login";
import Register from "./components/Register";

function App() {
  // Стейты для хранения токена и имени пользователя
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState(null);

  // Функция для обработки успешного логина: сохраняем токен и имя пользователя
  const handleLogin = (jwtToken, username) => {
    setToken(jwtToken); // Сохраняем токен для дальнейших запросов
    setUsername(username); // Сохраняем имя пользователя
  };

  return (
    <div className="App">
      <div className="container d-flex flex-column justify-content-center align-items-center vh-100">
        {token ? (
          // Если пользователь аутентифицирован (есть токен), отображаем компонент чата
          <Chat username={username} token={token} />
        ) : (
          // Если пользователь не аутентифицирован, показываем формы логина и регистрации
          <div className="row w-100">
            <div className="col-md-6 mb-4">
              <Login onLogin={handleLogin} />
            </div>
            <div className="col-md-6 mb-4">
              <Register />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
