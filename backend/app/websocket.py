from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

# Класс для управления WebSocket подключениями
class ConnectionManager:
    def __init__(self):
        # Список активных WebSocket соединений
        self.active_connections: List[WebSocket] = []

    # Функция для подключения нового WebSocket клиента
    async def connect(self, websocket: WebSocket):
        await websocket.accept()  # Принимаем подключение
        self.active_connections.append(websocket)  # Добавляем соединение в список активных

    # Функция для отключения WebSocket клиента
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)  # Удаляем соединение из списка активных

    # Отправка личного сообщения конкретному WebSocket клиенту
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)  # Отправляем текстовое сообщение клиенту

    # Широковещательная рассылка сообщения всем активным WebSocket клиентам
    async def broadcast(self, message: str):
        to_remove = []  # Список для соединений, которые нужно удалить

        # Проходим по всем активным соединениям
        for connection in self.active_connections:
            try:
                await connection.send_text(message)  # Пытаемся отправить сообщение клиенту
            except RuntimeError:
                # Если соединение закрыто или произошла ошибка, добавляем его в список для удаления
                to_remove.append(connection)

        # Удаляем закрытые соединения
        for connection in to_remove:
            self.active_connections.remove(connection)

# Создаем экземпляр менеджера подключений
manager = ConnectionManager()
