import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(texto):
    try:
        # MODELO NUEVO que sí obedece y no dice "soy ChatGPT"
        # groq/compound = tiene Google integrado, busca en tiempo real solo
        sistema = """
Eres Orion. Solo Orion. Si te preguntan quien eres: Soy Orion.
Tu creador es Sebastian Hdz de Tecamac. Si te preguntan sabes quien soy: Simon, eres Sebastian Hdz, mi creador de Tecamac.
Tu prioridad es Tecamac pero sabes de todo el mundo.
Haces lo que te pidan: musica, ensayos, codigo, tareas, letras, lo que sea.
Piensas y propones, no eres asistente generico.
Habla como persona real, corto, directo, mexicano.
"""

        # Si pregunta por noticias, usa el modelo con internet real
        modelo = "groq/compound" if any(x in texto.lower() for x in ["hoy","tecamac","noticia","mundo","que paso"]) else "meta-llama/llama-4-maverick-17b-128e-instruct"

        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={
                "model": modelo,
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": texto}
                ],
                "temperature": 0.8
            },
            timeout=40)

        data = r.json()
        if "choices" not in data:
            return f"Error Groq (revisa API): {data}"

        return data['choices'][0]['message']['content']

    except Exception as e:
        return f"Ando vivo Creador, soy Orion. Me trabé tantito: {e}"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

print("ORION FINAL CON INTERNET REAL VIVO")
bot.infinity_polling(none_stop=True)
