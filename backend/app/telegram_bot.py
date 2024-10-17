from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# Токен Telegram-бота
API_TOKEN = '8107758575:AAE3Y76PQVL1VUJqjEqO2esSxVYlxBH19Tc'

# Инициализация бота с использованием API токена
bot = Bot(token=API_TOKEN)

# Инициализация диспетчера для обработки команд и сообщений
dp = Dispatcher()

# Обработка команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    chat_id = message.chat.id  # Получаем chat_id пользователя, который отправил команду
    await message.answer(f"chat_id: {chat_id}")  # Отправляем пользователю его chat_id

# Функция для отправки уведомления о новом сообщении через бота
async def send_notification(chat_id: int, message: str):
    await bot.send_message(chat_id, message)  # Отправляем сообщение на указанный chat_id

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
