import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

web_app = Flask(__name__)

@web_app.route('/')
def health():
    return "SMM Bot is online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("PROVIDER_API_URL")
API_KEY = os.getenv("PROVIDER_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to QuickBoost SMM Store!\n\n"
        "📌 To place an order, use:\n"
        "/order <service_id> <instagram_link> <quantity>\n\n"
        "Example:\n"
        "/order 1 https://instagram.com/yourhandle 1000"
    )

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("❌ Format: /order <service_id> <link> <quantity>")
        return
    
    service, link, quantity = context.args[0], context.args[1], context.args[2]
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
            await update.message.reply_text(f"✅ Order Placed Successfully!\nOrder ID: {res['order']}")
        else:
            await update.message.reply_text(f"⚠️ Provider Message: {res.get('error', 'Check balance or link')}")
    except Exception:
        await update.message.reply_text("❌ Failed to reach the wholesale provider server.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("order", order))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    main()
  
