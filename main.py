import telebot, requests, os, sys, threading
from flask import Flask

# 1. Render အတွက် Flask Server (Web Service အနေနဲ့ Run ရန်)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

# 2. Token စစ်ဆေးခြင်း
TOKEN = os.environ.get('TOKEN', '').strip()
if not TOKEN:
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)

# 3. AI ဖြေကြားခြင်း Function
def get_ai_reply(prompt):
    try:
        r = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(prompt)}", timeout=20)
        return r.text[:300] if r.status_code == 200 else "AI စနစ် ခေတ္တရပ်နေပါသည်။"
    except:
        return "AI ဆီက အဖြေမရလို့ပါ။"

# 4. Command Handlers
@bot.message_handler(commands=['start'])
def start(message):
    msg = """
🤖 Bot အဆင်သင့်ဖြစ်ပါပြီ!

အသုံးပြုနိုင်သော Commands:
📸 /photo [အကြောင်းအရာ] - ပုံထုတ်ရန်
🎥 /video [အကြောင်းအရာ] - ဗီဒီယိုထုတ်ရန်
🧠 /ai [မေးခွန်း] - AI မေးရန်
    """
    bot.reply_to(message, msg)

@bot.message_handler(commands=['photo'])
def handle_photo(message):
    query = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else "art"
    bot.send_chat_action(message.chat.id, 'upload_photo')
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(query)}?enhance=true"
    try:
        bot.send_photo(message.chat.id, url, caption=f"📸 ရလဒ်: {query}")
    except:
        bot.reply_to(message, "ပုံထုတ်မရပါ၊ နောက်တစ်ခါ ထပ်ကြိုးစားကြည့်ပါ။")

@bot.message_handler(commands=['video'])
def handle_video(message):
    query = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else "art"
    bot.send_chat_action(message.chat.id, 'upload_video')
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(query)}?model=flux&enhance=true"
    try:
        bot.send_video(message.chat.id, url, caption=f"🎥 ရလဒ်: {query}")
    except:
        bot.reply_to(message, "ဗီဒီယိုထုတ်မရပါ၊ နောက်တစ်ခါ ထပ်ကြိုးစားကြည့်ပါ။")

@bot.message_handler(commands=['ai'])
def handle_ai(message):
    bot.send_chat_action(message.chat.id, 'typing')
    query = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else "Hello"
    bot.reply_to(message, get_ai_reply(query))

# 5. Main Execution
if __name__ == '__main__':
    # Flask ကို Thread ဖြင့် Run
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    
    print("✅ Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.infinity_polling(none_stop=True)
  
