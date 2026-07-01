import telebot, requests, os, sys, threading
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

TOKEN = os.environ.get('TOKEN', '').strip()
bot = telebot.TeleBot(TOKEN)
OWNERS = [8533383380, 7771663458]

# 1. AI အတွက် ဘာသာပြန်ခြင်း (မြန်မာ -> အင်္ဂလိပ်)
def translate_to_english(text):
    try:
        r = requests.get(f"https://text.pollinations.ai/prompt/Translate to English: {text}", timeout=10)
        return r.text.strip()
    except: return text

# 2. Main Logic (Forward & Commands)
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Owner ဆီ Forward လုပ်ခြင်း
    if message.chat.id not in OWNERS:
        for owner_id in OWNERS:
            try: bot.forward_message(owner_id, message.chat.id, message.message_id)
            except: pass

    # Commands များ
    if message.text:
        text = message.text
        if text.startswith('/start'):
            bot.reply_to(message, "Commands:\n/photo [ခေါင်းစဉ်] - ပုံထုတ်ရန်\n/video [ခေါင်းစဉ်] - ဗီဒီယိုလင့်ခ်ထုတ်ရန်\n/ai [မေးခွန်း] - AI မေးရန်")
        
        elif text.startswith('/ai'):
            query = text.split(' ', 1)[1] if len(text.split(' ', 1)) > 1 else "Hello"
            bot.send_chat_action(message.chat.id, 'typing')
            eng = translate_to_english(query)
            reply = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(eng)}", timeout=15).text
            bot.reply_to(message, reply[:300])

        elif text.startswith('/photo'):
            query = text.split(' ', 1)[1] if len(text.split(' ', 1)) > 1 else "art"
            eng = translate_to_english(query)
            url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(eng)}?enhance=true"
            bot.send_photo(message.chat.id, url, caption=f"📸 {query}")

        elif text.startswith('/video'):
            query = text.split(' ', 1)[1] if len(text.split(' ', 1)) > 1 else "art"
            eng = translate_to_english(query)
            url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(eng)}?model=flux"
            bot.reply_to(message, f"🎥 ဗီဒီယို ရလဒ်လင့်ခ်:\n{url}")

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    print("✅ Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.infinity_polling(none_stop=True)
      
