from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# Секретный ключ и алгоритм для шифрования JWT-токенов
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена в минутах

# Контекст для работы с хешированием паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Указываем FastAPI, что будем использовать OAuth2 для аутентификации с использованием токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для проверки пароля: сравнивает обычный пароль с хешированным
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функция для создания JWT-токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()  # Копируем данные для шифрования
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Если передан срок действия токена
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Стандартный срок жизни токена
    to_encode.update({"exp": expire})  # Добавляем время истечения токена
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Шифруем токен с использованием алгоритма
    return encoded_jwt

# Асинхронная функция для получения текущего пользователя по токену
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Ошибка валидации, если токен неверный или недействительный
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодируем токен, чтобы получить информацию о пользователе
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # Извлекаем имя пользователя из токена
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception  # Ошибка, если токен недействителен
    user = crud.get_user_by_username(db, username=username)  # Получаем пользователя из базы данных
    if user is None:
        raise credentials_exception  # Если пользователь не найден
    return user  # Возвращаем текущего пользователя
