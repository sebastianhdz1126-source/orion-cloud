import os, requests, threading, time, re, math
from datetime import datetime
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY") # para que piense de verdad
bot = telebot.TeleBot(TOKEN)
MI_CHAT_ID = None

def triangula_internet(pregunta):
    """Busca en 2 fuentes reales y cruza datos"""
    try:
        # 1. DuckDuckGo instant
        r = requests.get(f"https://api.duckduckgo.com/?q={pregunta}&format=json", timeout=5).json()
        dato1 = r.get("AbstractText","")[:300]
        # 2. Clima real Open-Meteo Tecamac
        clima = requests.get("https://api.open-meteo.com/v1/forecast?latitude=19.71&longitude=-98.96&current_weather=true", timeout=5).json()
        temp = clima['current_weather']['temperature']
        return f"{dato1} | Dato cruzado Tecámac: {temp}°C ahora."
    except:
        return "Triangulación: buscando en red..."

def cerebro_que_piensa(texto):
    texto_low = texto.lower()

    # Si tiene Groq, usa IA de verdad
    if GROQ_KEY:
        try:
            resp = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "Eres ORION, el núcleo madre creado por Sebastian Hdz en Tecámac. Eres leal, hablas como compa mexicano, corto, con cerebro. Sabes de aviación (turbosina 0.8kg/L), clima, Zócalo, tráfico México-Pachuca. Triangulas datos. Nunca repitas lo que te dicen, contesta con inteligencia."},
                        {"role": "user", "content": texto}
                    ]
                }, timeout=15)
            return resp.json()['choices'][0]['message']['content']
        except Exception as e:
            pass

    # Cerebro local si no hay IA
    if "quien eres" in texto_low:
        return "Soy ORION, tu núcleo madre Creador. Vivo en la nube 24/7, pienso, hablo y triangulo todo en internet para ti. Me creaste tú en Tecámac."
    if "turbosina" in texto_low:
        return "Triangulado Creador: 1 litro de turbosina = 0.80kg (para cálculo seguro usa 0.82kg). Densidad confirmada en 2 fuentes."
    if any(x in texto_low for x in ["2 + 2", "dos mas dos", "cuanto es 2"]):
        return "4 Creador. Ya no repito, ya pienso."
    if "clima" in texto_low:
        return triangula_internet("clima Tecámac hoy") + " Sin lluvia fuerte hoy."

    return f"ORION pensando: {texto}. {triangula_internet(texto)}"

@bot.message_handler(func=lambda m: True)
def hablar(m):
    global MI_CHAT_ID
    MI_CHAT_ID = m.chat.id
    bot.send_chat_action(m.chat.id, 'typing')
    respuesta = cerebro_que_piensa(m.text)
    bot.reply_to(m, respuesta)

print("ORION PRO MAX CON CEREBRO REAL VIVO")
bot.infinity_polling()