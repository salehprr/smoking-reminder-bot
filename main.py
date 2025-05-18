
import logging
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import time
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = None  # بعد از اجرای /start پر میشه

messages = [
    "🧘‍♂️ یه نفس عمیق... میل به سیگار می‌گذره.",
    "🔥 تو قوی‌تری از این عادت. فقط ۵ دقیقه صبر کن.",
    "💪 امروزم داری بهتر از دیروز می‌شی.",
    "🚭 یه نخ کمتر، یه گام به سلامتی نزدیک‌تر.",
    "👏 به خودت افتخار کن. ترک سخته ولی تو داری انجامش می‌دی."
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot = Bot(token=TOKEN)
scheduler = BackgroundScheduler()

def send_reminder():
    if CHAT_ID:
        from random import choice
        bot.send_message(chat_id=CHAT_ID, text=choice(messages))

async def start(update, context):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await context.bot.send_message(chat_id=CHAT_ID, text="👋 سلام! از حالا روزی ۵ بار بهت یادآوری می‌کنم که کمتر سیگار بکشی.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    scheduler.add_job(send_reminder, 'cron', hour=9, minute=0)
    scheduler.add_job(send_reminder, 'cron', hour=12, minute=0)
    scheduler.add_job(send_reminder, 'cron', hour=15, minute=0)
    scheduler.add_job(send_reminder, 'cron', hour=18, minute=0)
    scheduler.add_job(send_reminder, 'cron', hour=21, minute=0)

    scheduler.start()
    app.run_polling()
