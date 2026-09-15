import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)
print(f"KEY GROQ: {'OK' if GROQ else 'VACIA'}")

def pensar(texto):
    if not GROQ:
        return "Creador, GROQ_API_KEY sigue vacía en Railway. Dale Deploy."
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "Eres ORION, núcleo madre creado por Sebastian Hdz en Tecámac. Eres inteligente, triangulas cualquier info, mexicano, corto."},
                    {"role": "user", "content": texto}
                ]
            }, timeout=20)
        data = r.json()
        if "choices" not in data:
            return f"Error Groq: {data}"
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error conectando a Groq: {e}"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

bot.infinity_polling(none_stop=True)