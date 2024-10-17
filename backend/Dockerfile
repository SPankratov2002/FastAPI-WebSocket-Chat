# Указываем базовый образ Python 3.10
FROM python:3.10-slim

# Устанавливаем переменную окружения для недопустимого поведения Python (не создавать pyc файлы)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . /app/

# Указываем порт, который будет использовать FastAPI
EXPOSE 8000

# Запускаем FastAPI приложение с помощью uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
