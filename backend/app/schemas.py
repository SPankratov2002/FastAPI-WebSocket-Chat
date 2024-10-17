from pydantic import BaseModel
from datetime import datetime


# Схема для создания пользователя (используется для получения данных при регистрации)
class UserCreate(BaseModel):
    username: str  # Имя пользователя
    email: str  # Email пользователя
    password: str  # Пароль пользователя (в исходном виде)

# Схема для возврата данных о пользователе (например, при запросе информации о пользователе)
class User(BaseModel):
    id: int  # Уникальный идентификатор пользователя
    username: str  # Имя пользователя
    email: str  # Email пользователя

    # Указывает Pydantic, что схема будет использовать ORM-модель (например, SQLAlchemy)
    class Config:
        orm_mode = True


# Схема для создания нового сообщения (используется при отправке сообщения)
class MessageCreate(BaseModel):
    sender_id: int  # ID отправителя
    receiver_id: int  # ID получателя
    message: str  # Текст сообщения

# Схема для возврата информации о сообщении
class Message(BaseModel):
    id: int  # Уникальный идентификатор сообщения
    sender_id: int  # ID отправителя
    receiver_id: int  # ID получателя
    message: str  # Текст сообщения
    timestamp: datetime  # Время отправки сообщения

    # Указывает Pydantic, что схема будет использовать ORM-модель (например, SQLAlchemy)
    class Config:
        from_attributes = True


# Схема для JWT-токена, возвращаемого при аутентификации
class Token(BaseModel):
    access_token: str  # Сам JWT-токен
    token_type: str  # Тип токена (например, Bearer)

# Схема для данных пользователя, извлеченных из токена при аутентификации (если требуется)
class TokenData(BaseModel):
    username: str | None = None  # Имя пользователя (может быть отсутствующим)
