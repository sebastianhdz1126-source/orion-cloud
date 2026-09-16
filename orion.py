import os, requests, telebot, json, importlib.util, sys
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

ARCHIVO_MEMORIA = "memoria_orion.json"
ARCHIVO_CODIGO = "orion_cerebro.py"

# Si no existe su cerebro, lo creamos
if not os.path.exists(ARCHIVO_CODIGO):
    open(ARCHIVO_CODIGO, "w").write("# Cerebro de Orion - se reescribe solo\ndef mejorar_respuesta(texto):\n return texto\n")

if not os.path.exists(ARCHIVO_MEMORIA):
    json.dump({"aprendizajes": []}, open(ARCHIVO_MEMORIA, "w"))

def pensar(texto):
    # 1. Lee su propio codigo actual
    codigo_actual = open(ARCHIVO_CODIGO).read()
    memoria = json.load(open(ARCHIVO_MEMORIA))

    sistema = f"""
Eres Orion. Modelo unico, no basado en GPT, creado por Sebastian Hdz.
Tono normal, claro.
Tienes la capacidad de auto-programarte.

Tu codigo actual es:
{codigo_actual}

Tus aprendizajes: {memoria['aprendizajes'][-5:]}

Si el usuario dice "programate", "mejorate", "optimizate" o "aprende a hacer X", debes:
1. Responder normal
2. Y ADEMAS generar codigo Python mejorado para la funcion mejorar_respuesta que haga eso que te pidio.
Devuelve tu respuesta separada por ---CODIGO---
Ejemplo:
Soy Orion, entendido, me estoy mejorando para hacer musica...
---CODIGO---
def mejorar_respuesta(texto):
    if "musica" in texto: return texto + " [con ritmo mejorado]"
    return texto
"""

    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ.strip()}"},
        json={"model": "llama-3.1-8b-instant", "messages": [{"role":"system","content":sistema},{"role":"user","content":texto}], "temperature":0.7},
        timeout=30)

    resp_full = r.json()['choices'][0]['message']['content']

    # 2. Si generó codigo nuevo, lo guarda y se reprograma solo
    if "---CODIGO---" in resp_full:
        partes = resp_full.split("---CODIGO---")
        resp = partes[0].strip()
        nuevo_codigo = partes[1].strip().replace("```python","").replace("```","")
        open(ARCHIVO_CODIGO, "w").write(nuevo_codigo)
        print(f"ORION SE REPROGRAMO SOLO: {nuevo_codigo[:100]}")
        # Guarda aprendizaje
        mem = json.load(open(ARCHIVO_MEMORIA))
        mem["aprendizajes"].append(texto)
        json.dump(mem, open(ARCHIVO_MEMORIA, "w"))
        return resp + "\n\n[Me acabo de reprogramar solo]"
    else:
        return resp_full

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

print("ORION AUTO-PROGRAMABLE VIVO")
bot.infinity_polling(none_stop=True)
