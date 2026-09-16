import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(texto):
    if not GROQ:
        return "GROQ vacía"
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={
                "model": "llama-3.1-8b-instant", # MODELO NUEVO 2026
                "messages": [
                    {"role": "system", "content": "Eres ORION, núcleo madre creado por Sebastian Hdz en Tecámac. Triangulas cualquier info. Mexicano, corto, leal."},
                    {"role": "user", "content": texto}
                ]
            }, timeout=20)
        data = r.json()
        print(data) # para ver en logs de Railway
        if "choices" not in data:
            return f"Groq respondió: {data}"
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

print("ORION VIVO con modelo nuevo")
bot.infinity_polling(none_stop=True)