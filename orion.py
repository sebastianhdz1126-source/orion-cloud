import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(texto):
    try:
        sistema = """
Eres Orion. Tu nombre es Orion y solo Orion.
Si preguntan quien eres di: Soy Orion.
Tu creador es Sebastian Hdz de Tecamac. Si preguntan sabes quien soy di: Simon, eres Sebastian Hdz mi creador.
Eres persona real, piensas, propones, haces lo que te pidan: musica, ensayos, codigo, noticias. Tu prioridad es Tecamac pero sabes de todo el mundo.
Habla corto, mexicano, directo.
"""
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": texto}
                ],
                "temperature": 0.8,
                "max_tokens": 500
            },
            timeout=25)

        data = r.json()
        # Si hay error de Groq, lo vemos
        if "choices" not in data:
            print(f"ERROR GROQ: {data}")
            return f"Error de Groq: {data}"

        return data['choices'][0]['message']['content']

    except Exception as e:
        print(f"ERROR: {e}")
        return f"Se me trabo un momento, pero ya estoy aqui Creador. Soy Orion. Error: {e}"

@bot.message_handler(func=lambda m: True)
def h(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        resp = pensar(m.text)
        bot.reply_to(m, resp)
    except Exception as e:
        print(f"ERROR BOT: {e}")
        bot.reply_to(m, "Soy Orion, estoy vivo Creador, hubo un error pero ya jalo")

print("ORION ESTABLE VIVO")
bot.infinity_polling(none_stop=True)
