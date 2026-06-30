import telebot, requests, time, threading, schedule, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Render ၏ Environment Variables မှ Token ကို တိုက်ရိုက်ယူပါသည်
TOKEN = os.environ.get('TOKEN')
MY_ID = 7771663458,8533383380
CHANNEL_ID = -1001003841480184
bot = telebot.TeleBot(TOKEN)
last_msg = {"text": None, "chat_id": None, "message_id": None}

# --- ၁။ Start Command ---
@bot.message_handler(commands=['start'])
def start(message):
    report = f"👤 အသစ်ဝင်လာသူ: {message.from_user.first_name}\nID: {message.from_user.id}"
    try: bot.send_message(MY_ID, report)
    except: pass
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Channel ကိုသွားရန်", url="https://t.me/BOTUAPTE"))
    bot.reply_to(message, "မင်္ဂလာပါ! ကျွန်ုပ်တို့၏ Channel ကို ဝင်ကြည့်နိုင်ပါတယ်ခင်ဗျာ။ 🫣", reply_markup=markup)

# --- ၂။ AI Chat (လူတိုင်းမေးနိုင်သည်) ---
@bot.message_handler(commands=['ai'])
def ai_chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    user_input = message.text.split(' ', 1)[1] if ' ' in message.text else "Hello"
    try:
        reply = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(user_input)}").text
        bot.reply_to(message, reply)
    except:
        bot.reply_to(message, "AI နဲ့ ချိတ်ဆက်လို့မရသေးလို့ပါခင်ဗျာ။ 🫣")

# --- ၃။ AI Media (ဆရာကြီးပဲ သုံးရမယ်) ---
@bot.message_handler(commands=['draw', 'video'])
def ai_media(message):
    if message.from_user.id != MY_ID:
        bot.reply_to(message, "ချောချောလေးမှ မဟုတ်တာ... အဲဒီတော့ သုံးလို့မရဘူးလေ 🫣")
        return
    bot.reply_to(message, "⏳ AI ပုံ/ဗီဒီယို ဖန်တီးနေသည်...")

# --- ၄။ Monitor & Auto-Reply ---
@bot.message_handler(func=lambda m: True)
def monitor_and_reply(message):
    if message.chat.id != MY_ID:
        try: bot.forward_message(MY_ID, message.chat.id, message.message_id)
        except: pass
    last_msg.update({"text": message.text, "chat_id": message.chat.id, "message_id": message.message_id})

def ai_companion():
    while True:
        time.sleep(60)
        if last_msg["text"]:
            try:
                p = f"Reply briefly as a close friend to: {last_msg['text']}"
                r = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(p)}").text
                bot.reply_to(telebot.types.Message(message_id=last_msg['message_id'], from_user=None, date=None, chat=telebot.types.Chat(id=last_msg['chat_id'], type='group'), content_type=None, options=None, json_string=None), r[:60])
            except: pass

# --- ၅။ Auto-Poster ---
def post(ptype):
    txt = "ဘဝအတွက် အကောင်းဆုံး သင်ခန်းစာများ"
    try:
        if ptype == "photo": bot.send_photo(CHANNEL_ID, "https://image.pollinations.ai/prompt/art?enhance=true", caption=txt)
        else: bot.send_video(CHANNEL_ID, "https://image.pollinations.ai/prompt/video?enhance=true", caption=txt)
    except: pass

schedule.every().day.at("08:00").do(post, "photo")
schedule.every().day.at("12:00").do(post, "video")
schedule.every().day.at("20:00").do(post, "video")

# --- Run ---
if __name__ == '__main__':
    threading.Thread(target=ai_companion, daemon=True).start()
    threading.Thread(target=lambda: [schedule.run_pending() or time.sleep(60) for _ in iter(int, 1)], daemon=True).start()
    bot.infinity_polling()
  
