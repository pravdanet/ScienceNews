from telegram import Bot
import asyncio
from dotenv import load_dotenv
import os
import sys

# Загрузка переменных из .env
load_dotenv()

# Получение ключа OpenAI
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Проверка наличия ключа
if not TOKEN:
    print("Ошибка: Ключ TELEGRAM_TOKEN не найден в файле .env")
    sys.exit(1)  # Завершение программы с кодом ошибки

CHANNEL_ID = "@scince_news_ru"  

async def send_message():
    bot = Bot(token=TOKEN)
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text="Привет, это тестовое сообщение от бота! 🚀"
    )

# Запуск асинхронной функции
asyncio.run(send_message())