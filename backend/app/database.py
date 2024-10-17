from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Строка подключения к локальной базе данных PostgreSQL, работающей в Docker-контейнере
DATABASE_URL = "postgresql://postgres:527983@localhost:5432/appchat"

# Создаем движок для подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для создания моделей ORM
Base = declarative_base()

# Зависимость для получения сессии базы данных
# Это функция, которая предоставляет сессию базы данных для использования в запросах
# Сессия автоматически закрывается после завершения запроса
def get_db():
    db = SessionLocal()  # Открываем сессию
    try:
        yield db  # Возвращаем сессию
    finally:
        db.close()  # Закрываем сессию после использования
