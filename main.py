import os
import threading
import requests
from flask import Flask
import telebot

# 1. Background web server to keep Render happy
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "SMM Bot is running live!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# 2. Hardcoded Credentials
BOT_TOKEN = "8619035406:AAHwRNkRdnYXZCMCN6dmOzPhpUPTlHQsmWw"
API_URL = "https://fansmm.in/api/v2"
API_KEY = "6c3c776b6dd4d16a04ad791d84b75359"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 Welcome to QuickBoost SMM Store!\n\n"
        "📌 To place an order, send:\n"
        "/order <service_id> <link> <quantity>\n\n"
        "Example:\n"
        "/order 1 https://instagram.com/yourhandle 1000"
    )

@bot.message_handler(commands=['order'])
def place_order(message):
    args = message.text.split()[1:]
    if len(args) < 3:
        bot.reply_to(message, "❌ Format: /order <service_id> <link> <quantity>")
        return

    service, link, quantity = args[0], args[1], args[2]
    payload = {
        "key": API_KEY,
        "action": "add",
        "service": service,
        "link": link,
        "quantity": quantity
    }

    try:
        res = requests.post(API_URL, data=payload, timeout=15).json()
        if "order" in res:
            bot.reply_to(message, f"✅ Order Placed Successfully!\nOrder ID: {res['order']}")
        else:
            bot.reply_to(message, f"⚠️ Provider Message: {res.get('error', 'Check balance or link')}")
    except Exception:
        bot.reply_to(message, "❌ Error connecting to wholesale server.")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.infinity_polling()
    
