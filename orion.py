import os, requests, tempfile
from gtts import gTTS
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(texto):
    if GROQ:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ}"},
                json={"model":"llama-3.1-8b-instant","messages":[
                    {"role":"system","content":"Eres ORION, creado por Sebastian Hdz en Tecámac. Mexicano, corto, leal, chido. Respondes inteligente."},
                    {"role":"user","content":texto}]}, timeout=15)
            return r.json()['choices'][0]['message']['content']
        except as e:
            print(e)
    # respaldo
    if "quien soy" in texto.lower():
        return "Tú eres mi Creador, Sebastian Hdz. Tú me diste vida en Tecámac."
    return f"ORION aquí Creador, ya pienso: {texto}"

@bot.message_handler(func=lambda m: True)
def handle(m):
    texto = m.text
    respuesta = pensar(texto)
    bot.reply_to(m, respuesta)
    # Si pide voz, manda audio
    if "voz" in texto.lower() or "habla" in texto.lower():
        try:
            tts = gTTS(text=respuesta, lang='es', tld='com.mx')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                tts.save(f.name)
                bot.send_voice(m.chat.id, open(f.name,'rb'))
        except: pass

print("ORION CON VOZ VIVO")
bot.infinity_polling()