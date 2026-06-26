import telebot, io, json, os
os.environ['no_proxy'] = '*' 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

TOKEN = '8068282768:AAFtpiEde3XjPhFhqh8-bKLXt9hzKl3Kzmk'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 6327721026
BINANCE_ID = "1241953283"
DB_FILE = 'users_data.json'

# --- قاعدة البيانات ---
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try: return {int(k): v for k, v in json.load(f).items()}
            except: return {}
    return {}

def save_data():
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_db, f, indent=4, ensure_ascii=False)

users_db = load_data()

# --- قائمة المنتجات مع الحسابات الكاملة ---
products = {
    "amazon": {"name": "Amazon Prime 6M", "price": 1.80, "items": ["Acc_Amz1", "Acc_Amz2"]},
    "expressvpn": {"name": "ExpressVPN 5D", "price": 0.45, "items": [
        "Email: nztzo@rindu.navsstore.com | Key: EZCRR4DSQG7ES3XMNJ8LAEC",
        "Email: jmzez@badai.navsstore.com | Key: EHSUIHSDXBB3KIAPF6RS2C8",
        "Email: yecez@peace.lockroom.cfd | Key: EWWEPMZ894WATCZNUYYW3YZ"
    ]},
    "netflix": {"name": "Netflix Profile", "price": 1.60, "items": ["NF_Prof1", "NF_Prof2"]},
    "adobe": {"name": "Adobe CC 1M", "price": 1.80, "items": ["Adobe_Acc1"]},
    "gemini": {"name": "Gemini Pro 18M", "price": 0.85, "items": [
        "Link: https://serviceactivation.google.com/subscription/new/AQCpiIHItLidFFvClEQE8Z96cNVfAvuq9SDp8CnlRGp3In2jZJI02jCXkbNl89CVsO4XQLnk9nSu5lr1w_i3q-d7OJdQtItz-Wr20MJ40ihij5657d0y60_FQs-KetaIZ5f7FP8zvOc9vrp2qAEpLBixw4bpc9-vN0ADk6j7Hi1gSfwt8Csxf7fI_pWQfGQx4dpShMNHs4_VIeLfFj3Comqc8UjZFZs20MllUi14LE5aNQT1PvcRvN0FjqJeLWYZUYST9TdaxV_apkaDlQ==",
        "Link: https://serviceactivation.google.com/subscription/new/AQCpiIHtctDQUndvPyFc8MOLf9KeP9RGcm8QhP7Sp-LvqgEJmWOeSgS8h-EbFwopnsTRrT-F9SafG61Kg8WE5HduEWW7G95ZkbJyM49YHm3_7QPamPEEiTlpA03rNW105KiPfucMxLqpI4Gs1ICuunJNotO0MB8duC1JkrAlnX1H5gZ7SCcQG0-PJuLuEij8iTLQKStqDFG2fQ43Ujpquxh69nKZjayBX5cA-ATKGsEMYMkNVgRA_FshbkzaF-9USniWgmIBnPCqtK8DYA=="
    ]},
    "emails": {"name": "Outlook/Hotmail", "price": 0.08, "items": [
        "phedracissyadelaide9224@hotmail.com|LQHUVGJG5h|OTP Link: https://dongvanfb.net/read_mail_box/",
        "cristalcaradocnaomie6740@hotmail.com|bFT8dhTpJi|OTP Link: https://dongvanfb.net/read_mail_box/"
    ]},
    "canva": {"name": "Canva Pro Admin", "price": 9.50, "items": ["Canva_Invite1"]},
    "capcut": {"name": "CapCut Pro 1M", "price": 2.00, "items": ["CC_Acc1"]}
}

def check_user(uid):
    if uid not in users_db:
        users_db[uid] = {"balance": 0.0, "orders": [], "joined": datetime.now().strftime("%d/%m/%Y")}
        save_data()

# --- الأوامر والتحكم ---
@bot.message_handler(commands=['start', 'menu'])
def menu(m):
    check_user(m.chat.id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🛍 المنتجات", callback_data="prod"),
        InlineKeyboardButton("💰 رصيدي", callback_data="bal"),
        InlineKeyboardButton("💳 إيداع", callback_data="dep")
    )
    bot.send_message(m.chat.id, f"🏠 متجر الخدمات الرقمية\n💵 رصيدك: ${users_db[m.chat.id]['balance']:.2f}", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    uid = c.message.chat.id
    if c.data == "prod":
        markup = InlineKeyboardMarkup()
        for k, v in products.items():
            markup.add(InlineKeyboardButton(f"{v['name']} (${v['price']})", callback_data=f"buy_{k}"))
        bot.edit_message_text("قائمة المنتجات المتاحة:", uid, c.message.id, reply_markup=markup)
    
    elif c.data.startswith("buy_"):
        key = c.data.split("_")[1]
        prod = products[key]
        if users_db[uid]["balance"] >= prod["price"]:
            if prod["items"]:
                item = prod["items"].pop(0)
                users_db[uid]["balance"] -= prod["price"]
                save_data()
                bot.send_message(uid, f"✅ تم الشراء بنجاح!\nالمنتج: {prod['name']}\nالبيانات: `{item}`", parse_mode='Markdown')
            else: bot.answer_callback_query(c.id, "❌ نفذت الكمية!")
        else: bot.answer_callback_query(c.id, "❌ رصيد غير كافٍ!")

    elif c.data == "bal":
        bot.answer_callback_query(c.id, f"رصيدك: ${users_db[uid]['balance']:.2f}", show_alert=True)
    
    elif c.data == "dep":
        bot.send_message(uid, f"🔶 أرسل المبلغ لـ Binance Pay:\n`{BINANCE_ID}`\nثم أرسل رقم العملية للمدير.", parse_mode='Markdown')

bot.infinity_polling()
