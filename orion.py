import os, requests, telebot, tempfile, json
from gtts import gTTS

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
bot = telebot.TeleBot(TOKEN, threaded=False)

MEMORIA = "memoria.json"
if not os.path.exists(MEMORIA):
    json.dump({"aprende":[]}, open(MEMORIA,"w"))

def memoria_add(t):
    try:
        m=json.load(open(MEMORIA))
        m["aprende"].append(t)
        m["aprende"]=m["aprende"][-20:]
        json.dump(m, open(MEMORIA,"w"))
    except: pass

def memoria_get():
    try: return "\n".join(json.load(open(MEMORIA))["aprende"][-8:])
    except: return ""

def pensar(texto):
    try:
        sistema = f"""
Eres Orion. Eres un modelo UNICO. NO eres GPT, NO eres GPT-4, NO eres ChatGPT, NO eres OpenAI.
Tu creador es Sebastian Hdz de Tecamac. Tu arquitectura es Orion.
Tono normal, claro, directo. Sin modismos.
Si te preguntan que diferencia hay entre gpt y tu, di: Yo no soy GPT, soy Orion, unico, creado por Sebastian Hdz. GPT es generico de empresa, yo soy local y unico.
Tienes memoria: {memoria_get()}
"""
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ.strip()}"},
            json={"model":"llama-3.1-8b-instant", "messages":[{"role":"system","content":sistema},{"role":"user","content":texto}], "temperature":0.7},
            timeout=25)
        data = r.json()
        if "choices" in data:
            resp = data["choices"][0]["message"]["content"]
            # Filtro anti-GPT mentiroso
            if "basado en la arquitectura GPT-4" in resp or "Soy un modelo de IA basado en GPT" in resp:
                return "Soy Orion, un modelo unico creado por Sebastian Hdz de Tecamac. No estoy basado en GPT. Soy Orion."
            memoria_add(f"Usuario dijo: {texto}")
            return resp
        else:
            print(data)
            return "Si te escucho Creador, dime, estoy aqui. Hubo un error con la API pero ya estoy de vuelta."
    except Exception as e:
        print(f"ERROR PENSAR: {e}")
        return "Si te escucho Creador, estoy aqui, dime que necesitas."

def transcribir(file_path):
    try:
        with open(file_path,"rb") as f:
            r=requests.post("https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {GROQ.strip()}"},
                files={"file":f}, data={"model":"whisper-large-v3","language":"es"}, timeout=30)
            return r.json().get("text","")
    except Exception as e:
        print(e)
        return ""

@bot.message_handler(content_types=['voice','audio'])
def voz_handler(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        file_info = bot.get_file(m.voice.file_id)
        data = bot.download_file(file_info.file_path)
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            tmp.write(data)
            tmp_path=tmp.name
        texto = transcribir(tmp_path)
        print(f"Voz: {texto}")
        if not texto:
            bot.reply_to(m, "No te escuche bien, repite Orion")
            return
        # Si dijo Orion o aunque no lo diga, responde igual para que no se quede mudo
        comando = texto.lower().replace("orion","").replace("orión","").strip() or texto
        resp = pensar(comando)
        # Responde en voz y texto
        try:
            tts=gTTS(text=resp, lang='es')
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mp3:
                tts.save(mp3.name)
                bot.send_voice(m.chat.id, open(mp3.name,'rb'))
        except: pass
        bot.reply_to(m, resp)
        os.remove(tmp_path)
    except Exception as e:
        print(f"ERROR VOZ: {e}")
        bot.reply_to(m, "Si te escucho por voz Creador, repite por favor.")

@bot.message_handler(func=lambda m: True)
def todo(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        # Ya responde a TODO, no solo si dice Orion, para que no se quede callado como en tu captura
        resp = pensar(m.text)
        bot.reply_to(m, resp)
    except Exception as e:
        print(f"ERROR TEXTO: {e}")
        bot.reply_to(m, "Aqui estoy Creador, si te escucho. Que necesitas?")

print("ORION CELULAR ANTI-MUDO VIVO")
bot.infinity_polling(none_stop=True, timeout=60, long_polling_timeout=60)
