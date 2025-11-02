import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
from flask import Flask

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)

# توکن و آیدی از متغیرهای محیطی
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# دستور استارت
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('👋 سلام! یک عکس برای من بفرست تا برای ادمین ارسال کنم.')

# دریافت عکس
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.message.chat_id
        # فوروارد عکس به ادمین
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text('✅ عکس شما برای ادمین ارسال شد!')
        logging.info(f"Photo forwarded from {chat_id} to admin {ADMIN_ID}")
    except Exception as e:
        logging.error(f"Error forwarding photo: {e}")
        await update.message.reply_text('❌ خطا در ارسال عکس!')

# سایر پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and not update.message.text.startswith('/'):
        await update.message.reply_text('لطفاً یک عکس بفرستید!')

# راه‌اندازی ربات
def run_bot():
    try:
        # ساخت اپلیکیشن
        application = Application.builder().token(TOKEN).build()
        
        # اضافه کردن هندلرها
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # شروع ربات
        logging.info("🤖 Bot is starting...")
        application.run_polling()
    except Exception as e:
        logging.error(f"Bot error: {e}")

# سرور Flask برای فعال نگه داشتن
@app.route('/')
def home():
    return "🤖 Bot is running successfully!"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    # بررسی وجود توکن و آیدی
    if not TOKEN or not ADMIN_ID:
        logging.error("❌ TOKEN or ADMIN_ID not set!")
        exit(1)
    
    logging.info(f"✅ Token: {TOKEN[:10]}...")
    logging.info(f"✅ Admin ID: {ADMIN_ID}")
    
    # اجرای ربات در ترد جداگانه
    from threading import Thread
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # اجرای سرور Flask
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
