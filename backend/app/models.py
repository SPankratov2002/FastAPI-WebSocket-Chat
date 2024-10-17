from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# Модель пользователя
class User(Base):
    __tablename__ = "users"  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор пользователя (ID)
    username = Column(String, unique=True, index=True)  # Уникальное имя пользователя
    email = Column(String, unique=True, index=True)  # Уникальный email пользователя
    hashed_password = Column(String)  # Хешированный пароль

# Модель сообщения
class Message(Base):
    __tablename__ = "messages"  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор сообщения (ID)
    sender_id = Column(Integer, ForeignKey("users.id"))  # ID отправителя сообщения, внешний ключ на таблицу пользователей
    receiver_id = Column(Integer, ForeignKey("users.id"))  # ID получателя сообщения, внешний ключ на таблицу пользователей
    message = Column(String)  # Текст сообщения
    timestamp = Column(DateTime, default=datetime.utcnow)  # Время отправки сообщения

    # Связи с моделью User, используем для доступа к данным отправителя и получателя
    sender = relationship("User", foreign_keys=[sender_id])  # Связь с пользователем-отправителем
    receiver = relationship("User", foreign_keys=[receiver_id])  # Связь с пользователем-получателем
