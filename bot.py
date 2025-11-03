import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دریافت توکن از متغیر محیطی
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر برای دریافت عکس"""
    user = update.message.from_user
    photo = update.message.photo[-1]  # بزرگترین سایز عکس
    
    logging.info(f"عکس دریافت شده از {user.first_name}")
    
    # دانلود عکس
    photo_file = await photo.get_file()
    await photo_file.download_to_drive('temp_photo.jpg')
    
    # ارسال عکس به کاربر
    await update.message.reply_photo(
        photo=open('temp_photo.jpg', 'rb'),
        caption="عکس شما دریافت شد و برگشت داده می‌شود!"
    )
    
    # پاک کردن فایل موقت
    os.remove('temp_photo.jpg')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر برای دستور /start"""
    await update.message.reply_text(
        "سلام! من یک ربات دریافت عکس هستم. \n"
        "یک عکس برای من بفرستید تا آن را به شما بازگردانم."
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر برای خطاها"""
    logging.error(f"خطا رخ داده: {context.error}")

def main():
    """تابع اصلی برای راه‌اندازی ربات"""
    if not TOKEN:
        logging.error("توکن ربات تنظیم نشده است!")
        return
    
    # ایجاد اپلیکیشن
    application = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Command("start"), start_command))
    
    # هندلر خطا
    application.add_error_handler(error_handler)
    
    # شروع ربات
    logging.info("ربات در حال راه‌اندازی است...")
    application.run_polling()

if __name__ == '__main__':
    main()
