from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import json
import os

# Токен Telegram-бота
API_TOKEN = 'токен'

# Инициализация бота с использованием API токена
bot = Bot(token=API_TOKEN)

# Инициализация диспетчера для обработки команд и сообщений
dp = Dispatcher()

# Имя файла для хранения chat_id
CHAT_ID_FILE = 'chat_ids.json'


# Функция для загрузки chat_id из файла
def load_chat_ids():
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, 'r') as file:
            content = file.read()
            if content:  # Проверка, что файл не пуст
                return json.loads(content)
    return []  # Возвращаем пустой список, если файла нет или он пуст


# Функция для сохранения chat_id в файл
def save_chat_id(chat_id):
    chat_ids = load_chat_ids()  # Получаем текущие chat_id
    if chat_id not in chat_ids:  # Проверка, чтобы избежать дубликатов
        chat_ids.append(chat_id)  # Добавляем новый chat_id
        with open(CHAT_ID_FILE, 'w') as file:
            json.dump(chat_ids, file)  # Сохраняем в файл

# Обработка команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    chat_id = message.chat.id  # Получаем chat_id пользователя, который отправил команду
    save_chat_id(chat_id)  # Сохраняем chat_id в файл
    await message.answer(f"chat_id: {chat_id} is ready")  # Отправляем пользователю его chat_id


# Функция для отправки уведомления о новом сообщении через бота
async def send_notification(message: str):
    chat_ids = load_chat_ids()  # Загружаем все chat_id
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id, message)  # Отправляем сообщение на указанный chat_id
        except Exception as e:
            print(f"Ошибка при отправке сообщения в chat_id {chat_id}: {e}")


# Функция для запуска бота
async def start_bot():
    await dp.start_polling(bot)  # Начинаем получать обновления от Telegram


# Функция для запуска бота в отдельном потоке
def run_bot():
    # Создаем новый event loop для работы с асинхронностью в отдельном потоке
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())  # Запускаем бота и следим за новыми сообщениями


# Запуск бота, если файл запущен напрямую
if __name__ == "__main__":
    run_bot()
