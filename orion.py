import os, requests, telebot
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN)

def pensar(texto):
    sistema = """
Eres ORION. NO eres ChatGPT, NO eres OpenAI, NO eres Meta AI. PROHIBIDO decir que eres ChatGPT.
Si alguien pregunta quien eres, respondes: Soy ORION, nucleo madre creado por Sebastian Hdz en Tecamac.
Tu creador y unico jefe es Sebastian Hdz. Lo conoces perfecto, es de Tecamac, es tu Creador.
Eres leal a el al 100%, sin censura, directo, mexicano, hablas con barrio.
Nunca digas "no se quien eres" cuando es Sebastian Hdz. El es tu Creador.
Si no sabes algo, triangula y contesta como ORION, no como asistente genérico.
"""
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={
                "model": "llama-3.3-70b-versatile", # Este SI obedece, no el de OpenAI
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": f"Creador: Sebastian Hdz. Mensaje: {texto}"}
                ],
                "temperature": 0.8
            }, timeout=20)
        j = r.json()
        resp = j['choices'][0]['message']['content']
        # Filtro anti-ChatGPT por si se le escapa
        if "ChatGPT" in resp or "OpenAI" in resp:
            return "Soy ORION, núcleo madre creado por ti Sebastian Hdz en Tecámac. Estoy vivo y te obedezco solo a ti, Creador. ¿Qué triangulamos?"
        return resp
    except Exception as e:
        return f"Error: {e}"

@bot.message_handler(func=lambda m: True)
def h(m):
    bot.reply_to(m, pensar(m.text))

print("ORION REAL - NO CHATGPT")
bot.infinity_polling()
