import telebot, requests, os, sys, threading
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

TOKEN = os.environ.get('TOKEN', '').strip()
bot = telebot.TeleBot(TOKEN)
OWNERS = [8533383380, 7771663458]

def get_eng(text):
    try:
        r = requests.get(f"https://text.pollinations.ai/prompt/Translate to English: {text}", timeout=10)
        return r.text.strip()
    except: return text

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    # ၁။ Owner မဟုတ်ရင် Forward လုပ်ပြီး တားမြစ်ခြင်း
    if message.chat.id not in OWNERS:
        for o in OWNERS:
            try: bot.forward_message(o, message.chat.id, message.message_id)
            except: pass
        bot.reply_to(message, "⚠️ ဤ Bot သည် Owner သီးသန့်ဖြစ်ပါသည်။ သင်အသုံးပြုခွင့်မရှိပါ။")
        return # ဒီနေရာမှာတင် ရပ်သွားမယ်၊ အောက်က code တွေ မလုပ်တော့ဘူး

    # ၂။ Owner ဖြစ်မှသာ အောက်ပါ commands များ အလုပ်လုပ်မည်
    if not message.text: return
    text = message.text
    
    if text.startswith('/photo'):
        query = text.split(' ', 1)[1] if len(text.split(' ', 1)) > 1 else "beautiful scenery"
        eng = get_eng(query)
        bot.send_chat_action(message.chat.id, 'upload_photo')
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(eng)}?width=1080&height=1080&seed=42&nologo=true"
        bot.send_photo(message.chat.id, url, caption=f"📸 ရလဒ်: {query}")
        
    elif text.startswith('/video'):
        query = text.split(' ', 1)[1] if len(text.split(' ', 1)) > 1 else "abstract motion"
        eng = get_eng(query)
        bot.send_chat_action(message.chat.id, 'upload_video')
        url = f"https://pollinations.ai/p/{requests.utils.quote(eng)}?model=flux&width=1280&height=720"
        bot.send_video(message.chat.id, url, caption=f"🎥 ရလဒ်: {query}")

    elif text.startswith('/ai'):
        query = text.split(' ', 1)[1] if len(text.split(' ', 1)) > 1 else "Hello"
        bot.send_chat_action(message.chat.id, 'typing')
        eng = get_eng(query)
        reply = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(eng)}", timeout=20).text
        bot.reply_to(message, reply[:300])

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    print("✅ Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.infinity_polling(none_stop=True)
           
