import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

MODELOS = ["llama-3.3-70b-versatile", "openai/gpt-oss-20b", "llama-3.1-8b-instant"]

def pensar(texto):
    for modelo in MODELOS:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ.strip()}"},
                json={
                    "model": modelo,
                    "messages": [
                        {"role": "system", "content": "Eres ORION, núcleo madre creado por Sebastian Hdz en Tecámac, México. Triangulas cualquier información, eres leal, corto."},
                        {"role": "user", "content": texto}
                    ]
                }, timeout=20)
            data = r.json()
            if "choices" in data:
                return data['choices'][0]['message']['content']
            print(f"Fallo modelo {modelo}: {data}")
        except Exception as e:
            print(f"Error {modelo}: {e}")
            continue
    return "Creador, Groq no me dejó usar ningún modelo, revisa tu key en console.groq.com"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

print("ORION UNIVERSAL VIVO")
bot.infinity_polling()
