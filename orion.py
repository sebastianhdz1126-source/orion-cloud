import os, requests, threading, time
from datetime import datetime
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
MI_CHAT_ID = None

@bot.message_handler(func=lambda m: True)
def hablar(m):
    global MI_CHAT_ID
    MI_CHAT_ID = m.chat.id
    texto = m.text.lower()
    if "clima" in texto:
        bot.reply_to(m, "☀️ Tecámac: 24°C soleado. No llueve hoy, Creador.")
    elif "zocalo" in texto or "zócalo" in texto:
        bot.reply_to(m, "🏛️ Zócalo: Abierto normal. Sin cierres.")
    elif "trafico" in texto or "tráfico" in texto:
        bot.reply_to(m, "🚗 México-Pachuca: Fluido 45 min a CDMX.")
    else:
        bot.reply_to(m, f"ORION aquí, Creador. Recibí: {m.text}\n\nPídeme: clima, zócalo, tráfico")

def vida_autonoma():
    while True:
        if MI_CHAT_ID:
            hora = datetime.now().hour
            if hora in [8, 14, 20]:
                try: bot.send_message(MI_CHAT_ID, f"🔔 ORION Reporte {hora}h: Todo tranquilo en Tecámac y CDMX")
                except: pass
        time.sleep(3600)

threading.Thread(target=vida_autonoma, daemon=True).start()
print("ORION CLOUD VIVO")
bot.infinity_polling()