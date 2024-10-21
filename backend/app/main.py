from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import models, schemas, crud, auth
from .database import engine, get_db
from fastapi import WebSocket, WebSocketDisconnect
import threading
from .telegram_bot import run_bot, send_notification
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import redis.asyncio as redis
from .websocket import manager

# Инициализируем базу данных
models.Base.metadata.create_all(bind=engine)

# OAuth2 схема для работы с токенами
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

redis_instance = None


# Настройка подключения к Redis
async def get_redis():
    global redis_instance
    if not redis_instance:
        redis_instance = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return redis_instance

# Создаем экземпляр FastAPI
app = FastAPI(
    openapi_schema={
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
        "security": [{"BearerAuth": []}]
    }
)

# Добавляем CORS для взаимодействия с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и др.)
    allow_headers=["*"],  # Разрешаем все заголовки
)


# Запуск Telegram-бота в отдельном потоке
def start_telegram_bot():
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()


# WebSocket для чата
@app.websocket("/ws/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, db: Session = Depends(get_db), redis=Depends(get_redis)):
    await manager.connect(websocket)  # Подключаем пользователя к менеджеру WebSocket соединений

    # Находим пользователя в базе данных по имени
    user = crud.get_user_by_username(db, username=username)
    if not user:
        await websocket.close(code=4001)  # Закрываем соединение, если пользователь не найден
        return

    # Сохраняем пользователя как активного в Redis
    await redis.set(f"user:{user.id}:active", "1")

    # Получаем старые сообщения для пользователя
    old_messages = crud.get_messages_between_users(db, user.id, receiver_id=None)

    # Асинхронная функция для отправки старых сообщений
    async def send_old_messages():
        for message in old_messages:
            sender = crud.get_user_by_id(db, message.sender_id)
            sender_name = sender.username if sender else "Unknown"
            await websocket.send_text(f"{sender_name}: {message.message}")

    try:
        # Параллельно отправляем старые сообщения и начинаем слушать новые
        send_old_task = asyncio.create_task(send_old_messages())

        while True:
            # Получаем новое сообщение от клиента
            data = await websocket.receive_text()

            # Сохраняем новое сообщение в базе данных
            message_data = schemas.MessageCreate(sender_id=user.id, receiver_id=2, message=data)
            crud.create_message(db=db, message=message_data)

            # Сохраняем сообщение в кэш Redis (опционально)
            await redis.rpush(f"chat:{user.id}:messages", data)

            # Устанавливаем TTL для сообщений (например, 1 день)
            await redis.expire(f"chat:{user.id}:messages", 86400)

            # Отправляем уведомление через Telegram-бота
            await send_notification(message=f"User {username} sent a message: {data}")

            # Разослать новое сообщение всем подключённым пользователям
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        # Когда пользователь отключается, удаляем его из активных пользователей в Redis
        await redis.delete(f"user:{user.id}:active")
        # Отключаем пользователя и оповещаем других пользователей
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} left the chat")

    # Ждем завершения отправки старых сообщений
    await send_old_task

# Эндпоинт для регистрации пользователя
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# Эндпоинт для авторизации (получение токена)
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Создаем токен
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Эндпоинт для получения данных о текущем пользователе (защищённый)
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = await auth.get_current_user(db, token)
    return current_user

# Эндпоинт для отправки сообщения
@app.post("/messages/", response_model=schemas.Message)
async def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to send this message")
    return crud.create_message(db=db, message=message)


# Эндпоинт для получения истории сообщений между пользователями
@app.get("/messages/{user_id}", response_model=list[schemas.Message])
async def get_messages(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.get_messages_between_users(db, current_user.id, user_id)

# Инициализация приложения и запуск бота
if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    start_telegram_bot()

    # Запуск FastAPI
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
