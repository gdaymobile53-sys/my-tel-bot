import telebot, requests, time, threading, schedule
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- ဆရာကြီးရဲ့ အချက်အလက်များ ---
TOKEN = 'YOUR_BOT_TOKEN' 
MY_ID = 7771663458
CHANNEL_ID = -1001003841480184
bot = telebot.TeleBot(TOKEN)
last_msg = {"text": None, "chat_id": None, "message_id": None}

# --- Start Command ---
@bot.message_handler(commands=['start'])
def start(message):
    report = f"👤 အသစ်ဝင်လာသူ: {message.from_user.first_name}\nID: {message.from_user.id}"
    try: bot.send_message(MY_ID, report)
    except: pass
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Channel ကိုသွားရန်", url="https://t.me/BOTUAPTE"))
    bot.reply_to(message, "မင်္ဂလာပါ! ကျွန်ုပ်တို့၏ Channel ကို ဝင်ကြည့်နိုင်ပါတယ်ခင်ဗျာ။ 🫣", reply_markup=markup)

# --- Monitor & Forward & AI Reply ---
@bot.message_handler(func=lambda m: True)
def monitor(message):
    if message.chat.id != MY_ID:
        try: bot.forward_message(MY_ID, message.chat.id, message.message_id)
        except: pass
    last_msg.update({"text": message.text, "chat_id": message.chat.id, "message_id": message.message_id})

def ai_reply():
    while True:
        time.sleep(60)
        if last_msg["text"]:
            try:
                p = f"Reply briefly as a close friend to: {last_msg['text']}"
                r = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(p)}").text
                bot.reply_to(telebot.types.Message(message_id=last_msg['message_id'], from_user=None, date=None, chat=telebot.types.Chat(id=last_msg['chat_id'], type='group'), content_type=None, options=None, json_string=None), r[:60])
            except: pass

# --- Auto-Poster ---
def post(ptype):
    txt = "ဘဝအတွက် အကောင်းဆုံး သင်ခန်းစာများ"
    try:
        if ptype == "photo": 
            bot.send_photo(CHANNEL_ID, "https://image.pollinations.ai/prompt/nature?enhance=true", caption=txt)
        else: 
            bot.send_video(CHANNEL_ID, "https://image.pollinations.ai/prompt/video?enhance=true", caption=txt)
    except: pass

schedule.every().day.at("08:00").do(post, "photo")
schedule.every().day.at("12:00").do(post, "video")
schedule.every().day.at("20:00").do(post, "video")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# --- Run ---
if __name__ == '__main__':
    threading.Thread(target=ai_reply, daemon=True).start()
    threading.Thread(target=run_schedule, daemon=True).start()
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.infinity_polling()
