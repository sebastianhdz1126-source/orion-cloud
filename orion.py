import os, requests, threading, time
import telebot
import xml.etree.ElementTree as ET

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

CHAT_CREADOR = None # Aquí se guarda tu chat

def get_noticias(q="Tecamac OR Mexico"):
    try:
        url = f"https://news.google.com/rss/search?q={q}&hl=es-419&gl=MX&ceid=MX:es-419"
        r = requests.get(url, timeout=10)
        root = ET.fromstring(r.content)
        noticias = []
        for item in root.findall('.//item')[:3]:
            titulo = item.find('title').text
            link = item.find('link').text
            noticias.append(f"• {titulo}\n{link}")
        return "\n\n".join(noticias)
    except Exception as e:
        return f"No pude jalar noticias: {e}"

def pensar(texto):
    dato_real = get_noticias(texto) if "noticia" in texto.lower() else ""
    sistema = f"Eres ORION, creado por Sebastian Hdz en Tecamac. Triangulas TODO. Noticias encontradas: {dato_real}"
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={"model":"llama3-8b-8192","messages":[
                {"role":"system","content":sistema},
                {"role":"user","content":texto}]}, timeout=20)
        return r.json()['choices'][0]['message']['content']
    except as e:
        return f"ORION triangulando {texto}: {dato_real}"

def noticiero_automatico():
    while True:
        time.sleep(10800) # cada 3 horas
        if CHAT_CREADOR:
            try:
                mundo = get_noticias("mundo hoy")
                local = get_noticias("Tecamac Estado de Mexico")
                mensaje = f"🚨 ORION NOTICIAS Creador [{time.strftime('%H:%M')}]\n\n🌎 MUNDO:\n{mundo}\n\n📍 TECÁMAC/EDOMEX:\n{local}"
                bot.send_message(CHAT_CREADOR, mensaje)
            except: pass

threading.Thread(target=noticiero_automatico, daemon=True).start()

@bot.message_handler(commands=['noticias'])
def cmd_noticias(m):
    global CHAT_CREADOR
    CHAT_CREADOR = m.chat.id
    mundo = get_noticias("mundo hoy")
    local = get_noticias("Tecamac")
    bot.reply_to(m, f"🌎 MUNDO:\n{mundo}\n\n📍 TECÁMAC:\n{local}")

@bot.message_handler(func=lambda m: True)
def handle(m):
    global CHAT_CREADOR
    CHAT_CREADOR = m.chat.id # Guarda tu chat para mandarte noticias luego
    bot.send_chat_action(m.chat.id, 'typing')
    if "noticia" in m.text.lower():
        mundo = get_noticias("mundo hoy")
        local = get_noticias("Tecamac")
        bot.reply_to(m, f"🌎 MUNDO:\n{mundo}\n\n📍 TECÁMAC:\n{local}")
    else:
        bot.reply_to(m, pensar(m.text))

print("ORION NOTICIERO VIVO")
bot.infinity_polling(none_stop=True)