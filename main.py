import telebot, requests, time, threading, schedule, os, sys
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Flask (Render မှာ Bot 24/7 run ဖို့အတွက်)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

# Setup
TOKEN = os.environ.get('TOKEN', '').strip()
if not TOKEN:
    print("❌ ERROR: TOKEN missing!")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)
OWNERS = [7771663458, 8533383380]
CHANNEL_ID = -1001003841480184
last_msg = {"text": None, "chat_id": None, "message_id": None}

# --- Functions ---
def post(ptype):
    txt = "ဘဝအတွက် အကောင်းဆုံး သင်ခန်းစာများ"
    try:
        url = "https://image.pollinations.ai/prompt/art?enhance=true" if ptype == "photo" else "https://image.pollinations.ai/prompt/video?enhance=true"
        if ptype == "photo":
            bot.send_photo(CHANNEL_ID, url, caption=txt, timeout=60)
        else:
            bot.send_video(CHANNEL_ID, url, caption=txt, timeout=60)
    except Exception as e:
        print(f"Post Error: {e}")

def ai_companion():
    while True:
        time.sleep(60)
        if last_msg["text"]:
            try:
                p = f"Reply as friend to: {last_msg['text']}"
                r = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(p)}", timeout=10).text
                bot.send_message(last_msg['chat_id'], r[:60], reply_to_message_id=last_msg['message_id'])
                last_msg["text"] = None
            except: pass

# --- Handlers ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Channel ကိုသွားရန်", url="https://t.me/BOTUAPTE"))
    bot.reply_to(message, "မင်္ဂလာပါ! Cherry  အလုပ်လုပ်နေပါပြီရှင့်။ 🫣", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def monitor(message):
    last_msg.update({"text": message.text, "chat_id": message.chat.id, "message_id": message.message_id})

# --- Main ---
if __name__ == '__main__':
    # Flask Server
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    
    # AI Companion
    threading.Thread(target=ai_companion, daemon=True).start()
    
    # Scheduler
    schedule.every().day.at("08:00").do(post, "photo")
    schedule.every().day.at("12:00").do(post, "video")
    schedule.every().day.at("20:00").do(post, "video")
    
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(60)
    threading.Thread(target=run_schedule, daemon=True).start()

    print("✅ Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
          
