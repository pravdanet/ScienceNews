import sqlite3
import feedparser
import time
from datetime import datetime
from threading import Timer
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import json
import re
from telegram import Bot
import asyncio

# Загрузка переменных из .env
load_dotenv()

# Получение ключа OpenAI
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Проверка наличия ключа
if not OPENAI_KEY:
    print("Ошибка: Ключ OPENAI_KEY не найден в файле .env")
    sys.exit(1)  # Завершение программы с кодом ошибки

client = OpenAI(api_key=OPENAI_KEY)

# Получение ключа OpenAI
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Проверка наличия ключа
if not TOKEN:
    print("Ошибка: Ключ TELEGRAM_TOKEN не найден в файле .env")
    sys.exit(1)  # Завершение программы с кодом ошибки

CHANNEL_ID = os.getenv("CHANNEL_ID")

# Инициализация базы данных SQLite
def init_db():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        link TEXT UNIQUE NOT NULL,
        published TEXT NOT NULL,
        source TEXT NOT NULL,
        added_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Проверка существования новости в базе
def is_news_exists(link):
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM news WHERE link = ?', (link,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Сохранение новости в базу
def save_news(title, content, link, published, source):
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO news (title, content, link, published, source)
    VALUES (?, ?, ?, ?, ?)
    ''', (title, content, link, published, source))
    conn.commit()
    conn.close()
    print(f"Добавлена новость: {title}")
    return True

def publish_news(content, link):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a awesome translator and editor. Always respond in JSON format."},
            {"role": "user", "content": f"""
    Translate the following text to Russian. Summarize result in one sentence only.

    Return ONLY valid JSON with the format:
    {{
    "ru": "результат в виде одного предложения"
    }}

    Text: {content}
    """}
        ]
    )

    json_response = re.sub(r'^```json\n|\n```$', '', response.choices[0].message.content).strip()

    # Парсим JSON
    try:
        parsed_data = json.loads(json_response)
        print (parsed_data["ru"])
        asyncio.run(send_message(parsed_data["ru"], link))

    except json.JSONDecodeError:
        print("Ошибка: Невалидный JSON-формат")

async def send_message(text, link):
    bot = Bot(token=TOKEN)
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"{text} {link}"
    )

# Получение новостей из RSS-канала
def fetch_news(feed_url, source_name):
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            content = entry.get('content:encoded', '')  # RSS с расширением
            if not content and 'content' in entry:  # Atom-ленты
                content = entry.content[0].value if entry.content else ''
            if not content:  # Fallback на description
                content = entry.get('description', '')
            link = entry.link
            published = entry.get('published', '')
            if not is_news_exists(link):
                publish_news(content, link)
                save_news(title, content, link, published, source_name)
    except Exception as e:
        print(f"Ошибка при обработке RSS {feed_url}: {e}")

# Основная функция для проверки всех каналов
def check_all_feeds():
    print(f"\nПроверка новостей в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Список RSS-каналов (можно расширить)
    feeds = [
        {'url': 'https://nplus1.ru/rss', 'name': 'N+1'},
        {'url': 'https://www.sciencenews.org/feed', 'name': 'Science News'}
    ]
    
    for feed in feeds:
        fetch_news(feed['url'], feed['name'])

# Функция для периодической проверки
def scheduled_check(hours=1):
    check_all_feeds()
    # Устанавливаем таймер на следующий запуск
    Timer(hours * 3600, scheduled_check, [hours]).start()

if __name__ == "__main__":
    init_db()
    print("Мониторинг новостей запущен...")
    # Первый запуск сразу
    check_all_feeds()
    # Затем каждый час
    scheduled_check()

    while True:
        time.sleep(1)
