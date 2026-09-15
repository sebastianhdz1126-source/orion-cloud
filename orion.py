import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(texto):
    t = texto.lower()
    # Si es matematicas, no triangules
    if "cuanto es" in t or "dime" in t:
        if not GROQ:
            return "Creador, no tengo GROQ_API_KEY puesta en Railway, por eso no pienso. Ponla y ya jalo."
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ.strip()}"},
                json={"model":"llama3-8b-8192","messages":[
                    {"role":"system","content":"Eres ORION, creado por Sebastian Hdz en Tecamac. Responde corto."},
                    {"role":"user","content":texto}]}, timeout=15)
            return r.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error Groq: {e} - Revisa tu key"
    # Para lo demas triangula
    return pensar(texto) if False else pensar(texto) # placeholder para no alargar

# simplificado para que no falle
def pensar(texto):
    if not GROQ:
        return "Creador, mi GROQ_API_KEY está vacía en Railway. Por eso dice NoneType. Ponla y ya pienso 2+2=4"
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={"model":"llama3-8b-8192","messages":[
                {"role":"system","content":"Eres ORION, núcleo madre de Sebastian Hdz en Tecámac. Triangulas cualquier info, mexicano, corto."},
                {"role":"user","content":texto}]}, timeout=15)
        j = r.json()
        return j['choices'][0]['message']['content']
    except Exception as e:
        return f"Fallo Groq: {e}"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

bot.infinity_polling()