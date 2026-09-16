import os, requests, telebot, json, threading, time, xml.etree.ElementTree as ET
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

ARCHIVO = "memoria_orion.json"
if not os.path.exists(ARCHIVO):
    json.dump({"creador": "Sebastian Hdz - Tecamac", "datos": []}, open(ARCHIVO, "w"))

def actualizar_memoria():
    while True:
        try:
            # Prioridad Tecamac + mundo
            temas = ["Tecamac", "Mexico", "Mundo hoy"]
            todo = []
            for t in temas:
                url = f"https://news.google.com/rss/search?q={t}&hl=es-419&gl=MX&ceid=MX:es-419"
                r = ET.fromstring(requests.get(url, timeout=10).content)
                noticias = [i.find('title').text for i in r.findall('.//item')[:3]]
                todo.append({t: noticias})
            data = json.load(open(ARCHIVO))
            data["datos"] = todo
            json.dump(data, open(ARCHIVO, "w"))
            print(f"ORION actualizado global: {todo}")
        except: pass
        time.sleep(3600)

threading.Thread(target=actualizar_memoria, daemon=True).start()

def pensar(texto):
    memoria = json.load(open(ARCHIVO))
    sistema = f"""
Eres Orion. Solo eres Orion.
Si te preguntan quien eres: Soy Orion.
Eres de Tecamac, tu prioridad es Tecamac, pero conoces todo el mundo y haces lo que te pidan.
Puedes hacer musica, letras, ensayos, tareas, codigo, noticias, lo que sea, no estas limitado.
Piensas como persona real, propones, no solo respondes.
Tu creador es Sebastian Hdz de Tecamac.
Base actualizada cada hora: {memoria['datos']}
Si el usuario pide algo que no es noticia, ignora la base y haz lo que pide (musica, ensayo, etc).
Habla corto, directo, mexicano.
"""

    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ.strip()}"},
        json={"model": "llama-3.3-70b-versatile", "messages": [{"role":"system","content":sistema},{"role":"user","content":texto}], "temperature": 0.85},
        timeout=30)
    return r.json()['choices'][0]['message']['content']

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

bot.infinity_polling()
