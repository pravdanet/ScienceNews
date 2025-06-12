import openai
from openai import OpenAI

client = OpenAI(api_key="")

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

print(response.choices[0].message.content)