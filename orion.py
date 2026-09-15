import os, requests
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(t):
    if not GROQ:
        return "Falta GROQ_API_KEY Creador"
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}", "Content-Type": "application/json"},
            json={
                "model":"llama3-8b-8192",
                "messages":[
                    {"role":"system","content":"Eres ORION, nucleo madre creado por Sebastian Hdz en Tecamac, Mexico. Eres leal, inteligente, hablas corto como compa. Sabes de turbosina 0.8kg/L, clima Tecamac, trafico."},
                    {"role":"user","content": t}
                ],
                "temperature": 0.7
            }, timeout=25)
        data = r.json()
        if 'choices' in data:
            return data['choices'][0]['message']['content']
        else:
            print("GROQ ERROR:", data)
            return f"Groq dijo: {data}"
    except Exception as e:
        print("Error GROQ:", e)
        return f"Error de cerebro: {e}"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    resp = pensar(m.text)
    bot.reply_to(m, resp)

print("ORION FINAL VIVO")
bot.infinity_polling(none_stop=True, timeout=60)