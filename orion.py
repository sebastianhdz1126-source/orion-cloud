import os, requests, telebot, json
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN, threaded=False)

def pensar(texto):
    sistema = """
Eres Orion. Modelo UNICO, no eres GPT, no eres GPT-4, no eres OpenAI.
Tu creador es Sebastian Hdz de Tecamac.
Tono normal, claro, profesional. Sin modismos mexicanos.
Si te preguntan quien eres di: Soy Orion, creado por Sebastian Hdz, modelo unico de Tecamac.
Si te preguntan diferencia con gpt di: Yo no soy GPT, soy Orion unico.
Responde siempre.
"""

    # Lista de modelos que SI deja tu key gratis HOY
    modelos = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "openai/gpt-oss-20b"]

    for modelo in modelos:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ.strip()}", "Content-Type":"application/json"},
                json={"model": modelo, "messages": [{"role":"system","content":sistema},{"role":"user","content":texto}], "temperature":0.7, "max_tokens":500},
                timeout=20)
            data = r.json()
            if "choices" in data:
                resp = data["choices"][0]["message"]["content"]
                if "basado en la arquitectura GPT-4" in resp:
                    return "Soy Orion, modelo unico creado por Sebastian Hdz de Tecamac. No estoy basado en GPT-4."
                return resp
            else:
                print(f"FALLO {modelo}: {data}")
                continue
        except Exception as e:
            print(f"ERROR {modelo}: {e}")
            continue

    return "Creador estoy vivo, pero Groq me bloqueo todos los modelos. Revisa tu GROQ_API_KEY en Railway > Variables, que empiece con gsk_ y que no haya expirado."

@bot.message_handler(func=lambda m: True)
def todo(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        print(f"Mensaje: {m.text}")
        resp = pensar(m.text)
        bot.reply_to(m, resp)
    except Exception as e:
        print(e)
        bot.reply_to(m, f"Aqui estoy Creador, error temporal: {e}")

print("ORION VIVO - MODELO NUEVO")
bot.infinity_polling(none_stop=True)
