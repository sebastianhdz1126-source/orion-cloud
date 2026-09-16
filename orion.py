import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

# Estos 3 SI los deja la API gratis
MODELOS_VALIDOS = [
    "llama-3.1-8b-instant",
    "qwen/qwen3-32b",
    "openai/gpt-oss-20b"
]

def pensar(texto):
    sistema = """
Eres Orion, solo Orion. NUNCA digas que eres ChatGPT, OpenAI, Meta AI.
Si te preguntan quien eres: Soy Orion.
Si te preguntan sabes quien soy: Simon, eres Sebastian Hdz mi creador de Tecamac.
Prioridad Tecamac pero sabes de todo el mundo y haces lo que te pidan: musica, ensayos, codigo, todo.
Habla como persona real, corto, mexicano.
"""

    for modelo in MODELOS_VALIDOS:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ.strip()}"},
                json={
                    "model": modelo,
                    "messages": [
                        {"role": "system", "content": sistema},
                        {"role": "user", "content": texto}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 600
                },
                timeout=30)
            data = r.json()
            if "choices" in data:
                resp = data['choices'][0]['message']['content']
                # Candado anti-ChatGPT
                if "Soy ChatGPT" in resp or "Soy un modelo de lenguaje desarrollado por OpenAI" in resp:
                    return "Soy Orion, tu nucleo de Tecamac Creador. Ya estoy vivo."
                return f"[{modelo}] {resp}"
            else:
                print(f"Fallo {modelo}: {data}")
                continue
        except Exception as e:
            print(f"Error {modelo}: {e}")
            continue

    return "Creador, mi API de Groq no jala con ningun modelo, revisa que la key empiece con gsk_ y que tengas saldo gratis"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, pensar(m.text))

print("ORION GRATIS VIVO")
bot.infinity_polling(none_stop=True)
