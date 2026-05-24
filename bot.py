import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# جلب التوكن من إعدادات البيئة (Environment Variables)
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = "1263442365"

# إعداد السجل (Logging) لتعرف إذا حدث أي خطأ في السيرفر
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 مشاركة رقم الهاتف", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    await update.message.reply_text("مرحباً JOKER! 🔐\nمن فضلك شارك رقم هاتفك:", reply_markup=keyboard)

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.message.from_user
    
    message = (
        f"📥 تم استلام رقم جديد!\n\n"
        f"👤 الاسم: {user.first_name}\n"
        f"🧑‍💻 اليوزر: @{user.username if user.username else 'لا يوجد'}\n"
        f"🆔 الآيدي: {user.id}\n"
        f"📞 الرقم: {contact.phone_number}\n"
        f"📅 التاريخ: {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    await context.bot.send_message(chat_id=ADMIN_ID, text=message)
    await update.message.reply_text("✅ تم استلام رقمك!\n⌛ انتظر حتى المراجعة...")

if __name__ == '__main__':
    if not TOKEN:
        print("خطأ: لم يتم العثور على التوكن!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.CONTACT, contact))
        print("البوت يعمل الآن على السيرفر يا JOKER...")
        app.run_polling()
