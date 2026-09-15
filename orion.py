import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)
print(f"GROQ cargada: {'SI' if GROQ else 'NO'} {str(GROQ)[:10] if GROQ else ''}")

def pensar(t):
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={"model":"llama3-8b-8192","messages":[
                {"role":"system","content":"Eres ORION, creado por Sebastian Hdz. Contesta corto y inteligente."},
                {"role":"user","content":t}]}, timeout=20)
        j = r.json()
        print(j)
        return j['choices'][0]['message']['content']
    except Exception as e:
        return f"Creador, error de cerebro: {e} | Raw: {r.text if 'r' in locals() else 'no resp'}"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.reply_to(m, pensar(m.text))

bot.infinity_polling()