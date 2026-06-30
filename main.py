import telebot, requests, time, threading, schedule, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Token ကို Render ၏ Environment Variable မှ ခေါ်ယူခြင်း
TOKEN = os.environ.get('TOKEN')
OWNERS = [7771663458, 8533383380] # ဆရာကြီးနှစ်ယောက်စလုံး
CHANNEL_ID = -1001003841480184

# Bot စတင်ခြင်း
bot = telebot.TeleBot(TOKEN)
last_msg = {"text": None, "chat_id": None, "message_id": None}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Channel ကိုသွားရန်", url="https://t.me/BOTUAPTE"))
    bot.reply_to(message, "မင်္ဂလာပါ! ကျွန်ုပ်တို့၏ Bot စနစ် စတင်အလုပ်လုပ်နေပါပြီခင်ဗျာ။ 🫣", reply_markup=markup)

@bot.message_handler(commands=['ai'])
def ai_chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    user_input = message.text.split(' ', 1)[1] if ' ' in message.text else "Hello"
    try:
        reply = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(user_input)}").text
        bot.reply_to(message, reply[:200])
    except: bot.reply_to(message, "AI စနစ် ခေတ္တရပ်နေပါတယ်ခင်ဗျာ။ 🫣")

@bot.message_handler(commands=['draw', 'video'])
def ai_media(message):
    if message.from_user.id not in OWNERS:
        bot.reply_to(message, "သုံးလို့မရဘူးလေ 🫣")
        return
    bot.reply_to(message, "⏳ AI ပုံ/ဗီဒီယို ဖန်တီးနေသည်...")

@bot.message_handler(func=lambda m: True)
def monitor(message):
    if message.chat.id not in OWNERS:
        try: bot.forward_message(OWNERS[0], message.chat.id, message.message_id)
        except: pass
    last_msg.update({"text": message.text, "chat_id": message.chat.id, "message_id": message.message_id})

def ai_companion():
    while True:
        time.sleep(60)
        if last_msg["text"]:
            try:
                p = f"Reply as friend to: {last_msg['text']}"
                r = requests.get(f"https://text.pollinations.ai/prompt/{requests.utils.quote(p)}").text
                bot.reply_to(telebot.types.Message(message_id=last_msg['message_id'], from_user=None, date=None, chat=telebot.types.Chat(id=last_msg['chat_id'], type='group'), content_type=None, options=None, json_string=None), r[:60])
            except: pass

def post(ptype):
    txt = "ဘဝအတွက် အကောင်းဆုံး သင်ခန်းစာများ"
    try:
        if ptype == "photo": bot.send_photo(CHANNEL_ID, "https://image.pollinations.ai/prompt/art?enhance=true", caption=txt)
        else: bot.send_video(CHANNEL_ID, "https://image.pollinations.ai/prompt/video?enhance=true", caption=txt)
    except: pass

schedule.every().day.at("08:00").do(post, "photo")
schedule.every().day.at("12:00").do(post, "video")
schedule.every().day.at("20:00").do(post, "video")

if __name__ == '__main__':
    threading.Thread(target=ai_companion, daemon=True).start()
    threading.Thread(target=lambda: [schedule.run_pending() or time.sleep(60) for _ in iter(int, 1)], daemon=True).start()
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.infinity_polling()
