import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import json
import re

# Загрузка переменных из .env
load_dotenv()

# Получение ключа OpenAI
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Проверка наличия ключа
if not OPENAI_KEY:
    print("Ошибка: Ключ OPENAI_KEY не найден в файле .env")
    sys.exit(1)  # Завершение программы с кодом ошибки

client = OpenAI(api_key=OPENAI_KEY)

text = "Un aereo di linea della compagnia Air India diretto in Inghilterra è precipitato subito dopo il decollo dalla città indiana di Ahmedabad. Lo riporta la tv indiana, che parla di 242 persone a bordo. Secondo il sito Flightradar24, il volo Air India n. AI171 ha trasmesso l'ultimo segnale pochi secondi dopo il decollo. L'aereo coinvolto è un Boeing 787-8 Dreamliner, diretto all'aeroporto londinese di Gatwick. È precipitato nei pressi della città di Meghani. Una colonna di fumo scuro si è sollevata dal luogo dell'impatto ed è visibile a chilometri di distanza. I soccorsi, con autopompe e ambulanze, sono intervenute subito sul luogo del disastro."

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

Text: {text}
"""}
    ]
)

json_response = re.sub(r'^```json\n|\n```$', '', response.choices[0].message.content).strip()

# Парсим JSON
try:
    parsed_data = json.loads(json_response)
    print (parsed_data)
    print (parsed_data["ru"])

except json.JSONDecodeError:
    print("Ошибка: Невалидный JSON-формат")