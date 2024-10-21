# WebSocket Chat Application

## Описание проекта

Это приложение представляет собой простой чат с использованием WebSocket для обмена сообщениями в реальном времени. Оно состоит из двух частей:
1. **Backend** — написан на FastAPI, включает в себя авторизацию пользователей, отправку сообщений и уведомления через Telegram-бота.
2. **Frontend** — написан на React, предоставляет пользовательский интерфейс для отправки и получения сообщений в режиме реального времени.

Также проект использует **Redis** для управления подключениями и Telegram-бот для уведомлений о новых сообщениях.

## Технологии

- **Backend**: FastAPI, PostgreSQL, Redis, WebSocket, Aiogram (Telegram Bot), Docker
- **Frontend**: React, Bootstrap, WebSocket

## Инструкции по запуску

# Установка Backend
1. Клонируйте репозиторий.
2. Перейдите в папку backend.
3. Установите виртуальное окружение и активируйте его:
```
python -m venv .venv
source .venv/bin/activate  # для Windows: .venv\Scripts\activate
```
4. Установите зависимости:
```
pip install -r requirements.txt
```
5. Запустите Redis (например, используя Docker):
```
docker run -d -p 6379:6379 redis
```
6. Запустите backend сервер:
```
uvicorn app.main:app --reload
```

# Установка Frontend
1. Перейдите в папку frontend.
2. Установите зависимости:
```
npm install
```
3. Запустите проект:
```
npm run dev
```

## Запуск и доступ
После успешного запуска backend и frontend частей, перейдите в браузер по адресу:
```
http://localhost:5173
```
Frontend будет взаимодействовать с backend для отправки сообщений и выполнения других операций.

## API Документация
Backend проект автоматически генерирует документацию для API, которую можно просмотреть по адресу:
```
http://127.0.0.1:8000/docs
```
Документация включает описание всех доступных эндпоинтов, их входные и выходные параметры.

