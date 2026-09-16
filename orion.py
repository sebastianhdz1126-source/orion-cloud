import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(texto):
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ.strip()}"},
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "Eres ORION, núcleo madre creado por Sebastian Hdz en Tecámac. Triangulas cualquier información, eres leal, mexicano, corto."},
                {"role": "user", "content": texto}
            ]
        }, timeout=20)
    data = r.json()
    return data['choices'][0]['message']['content'] if "choices" in data else f"Error Groq: {data}"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.reply_to(m, pensar(m.text))

bot.infinity_polling()
