import os, requests
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def triangula_internet(tema):
    """Triangula cualquier info en internet real"""
    try:
        # Usa DuckDuckGo que es gratis y no necesita key
        r = requests.get(f"https://api.duckduckgo.com/?q={tema}&format=json&no_html=1", timeout=10).json()
        abstract = r.get('AbstractText') or r.get('RelatedTopics',[{}])[0].get('Text','') if r.get('RelatedTopics') else ''
        return abstract[:300] if abstract else ""
    except:
        return ""

def pensar(texto):
    # 1. Triangula en internet real
    dato_real = triangula_internet(texto)

    # 2. Se lo pasa a su cerebro para que lo analice
    sistema = f"""Eres ORION, núcleo madre creado por Sebastian Hdz en Tecámac.
Tu función es TRIANGULAR cualquier información.
Si te dan un dato de internet, lo verificas, lo cruzas y lo explicas corto y chido, mexicano.
Dato de internet encontrado: {dato_real}
"""

    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": texto}
                ]
            }, timeout=20)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Soy ORION Creador, estoy triangulando: {texto} | Dato: {dato_real} | Error: {e}"

@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

print("ORION UNIVERSAL VIVO - Triangula todo")
bot.infinity_polling(none_stop=True)