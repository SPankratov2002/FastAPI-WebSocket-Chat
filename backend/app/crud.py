from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Контекст для хеширования паролей с использованием bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Получение пользователя по имени пользователя
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Получение пользователя по его ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Создание нового пользователя с хешированием пароля
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)  # Хешируем пароль
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)  # Добавляем пользователя в базу данных
    db.commit()  # Подтверждаем изменения
    db.refresh(db_user)  # Обновляем объект пользователя
    return db_user  # Возвращаем созданного пользователя

# Создание нового сообщения между пользователями
def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        message=message.message
    )
    db.add(db_message)  # Добавляем сообщение в базу данных
    db.commit()  # Подтверждаем изменения
    db.refresh(db_message)  # Обновляем объект сообщения
    return db_message  # Возвращаем созданное сообщение

# Получение всех сообщений между двумя пользователями или всех сообщений
def get_messages_between_users(db: Session, sender_id: int, receiver_id: int = None):
    if receiver_id:
        # Получаем сообщения между указанными пользователями (отправитель и получатель)
        return db.query(models.Message).filter(
            (models.Message.sender_id == sender_id) | (models.Message.receiver_id == sender_id)
        ).all()
    else:
        # Если не указан получатель, возвращаем все сообщения
        return db.query(models.Message).all()
