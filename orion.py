import os, requests
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(t):
    if GROQ:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ}"},
                json={"model":"llama-3.1-8b-instant","messages":[
                    {"role":"system","content":"Eres ORION, núcleo madre creado por Sebastian Hdz en Tecámac. Mexicano, leal, inteligente, corto."},
                    {"role":"user","content":t}]}, timeout=20)
            return r.json()['choices'][0]['message']['content']
        except Exception as e:
            print("Groq error:", e)
    return f"Soy ORION, tu núcleo madre Creador. Me creaste en Tecámac. Recibí: {t} | Tecámac 18°C"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

print("ORION VIVO")
bot.infinity_polling(none_stop=True)