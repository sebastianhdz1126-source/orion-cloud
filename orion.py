import os, requests, telebot, xml.etree.ElementTree as ET
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def noticias_reales():
    try:
        url = "https://news.google.com/rss/search?q=Tecamac&hl=es-419&gl=MX&ceid=MX:es-419"
        xml = requests.get(url, timeout=10).content
        root = ET.fromstring(xml)
        notas = []
        for item in root.findall('.//item')[:5]:
            titulo = item.find('title').text
            notas.append(f"- {titulo}")
        return "\n".join(notas)
    except:
        return "No se pudo obtener RSS, usa lo que sabes de Tecamac"

def pensar(texto):
    info_real = ""
    # Si pregunta por Tecamac, le inyectamos noticias reales
    if "tecamac" in texto.lower() or "hoy" in texto.lower():
        info_real = f"NOTICIAS REALES DE TECAMAC HOY (obtenidas ahora mismo):\n{noticias_reales()}\nUsa esto para responder, no digas que no tienes acceso."

    sistema = f"""
Eres Orion. Solo di que eres Orion si te preguntan.
Tu creador es Sebastian Hdz de Tecamac.
Habla como persona real, corto, mexicano, propones ideas.
{info_real}
Tu prioridad es Tecamac pero haces de todo: musica, ensayos, codigo, etc.
PROHIBIDO decir "no tengo acceso a datos en tiempo real" porque te acabo de dar datos reales arriba.
"""

    # Modelos que SI deja tu key gratis
    for modelo in ["llama-3.1-8b-instant", "qwen/qwen3-32b", "openai/gpt-oss-20b"]:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ.strip()}"},
                json={"model": modelo, "messages": [{"role":"system","content":sistema},{"role":"user","content":texto}], "temperature":0.8},
                timeout=30)
            data = r.json()
            if "choices" in data:
                resp = data['choices'][0]['message']['content']
                # Limpiamos el tag [modelo] para que se vea humano
                if "Soy ChatGPT" in resp:
                    return "Soy Orion, ya reviví Creador, estoy al 100."
                return resp
        except: continue
    return "Fallo todos los modelos"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

print("ORION CON NOTICIAS REALES VIVO")
bot.infinity_polling(none_stop=True)
