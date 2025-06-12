from telegram import Bot
import asyncio

TOKEN = ""
CHANNEL_ID = "@scince_news_ru"  

async def send_message():
    bot = Bot(token=TOKEN)
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text="Привет, это тестовое сообщение от бота! 🚀"
    )

# Запуск асинхронной функции
asyncio.run(send_message())