from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ضع التوكن الخاص بك هنا
TOKEN = '8507097163:AAFFUKzBzYLeE9HAgT-M-xj9SSkfRDu3Mjg'

# قاعدة بيانات الدروس (أضف روابط الدرايف الخاصة بك هنا)
LESSONS = {
    "logic": "https://drive.google.com/your-logic-link",
    "algo": "https://drive.google.com/your-algo-link",
    "structure": "https://drive.google.com/your-structure-link"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إنشاء الأزرار التفاعلية
    keyboard = [
        [InlineKeyboardButton("📐 دروس المنطق التعاقبي", callback_query_data='logic')],
        [InlineKeyboardButton("💻 خوارزميات ومخططات", callback_query_data='algo')],
        [InlineKeyboardButton("🏗️ هندسة الحاسوب", callback_query_data='structure')],
        [InlineKeyboardButton("👨‍💻 المطور: YCan", url='https://instagram.com/your_profile')] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    user = update.effective_user
    await update.message.reply_text(
        f"مرحباً {user.first_name} في مساعد MI L1!\nاختر الدرس الذي تحتاجه من الأزرار بالأسفل:",
        reply_markup=reply_markup
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # لإخفاء علامة التحميل من الزر

    # إرسال الرابط بناءً على الزر المضغوط مع لمسة جمالية
    lesson_key = query.data
    if lesson_key in LESSONS:
        link = LESSONS[lesson_key]
        message = f"✅ إليك الرابط المطلوب:\n{link}\n\n🤖 مبرمج بواسطة: Abderahime Mansouri"
        await query.edit_message_text(text=message)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    print("🚀 البوت يعمل الآن.. اذهب وجربه!")
    app.run_polling()

if __name__ == '__main__':
    main()



import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# سيرفر وهمي لإبقاء Render سعيداً
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# تشغيل السيرفر في خلفية البوت
threading.Thread(target=run_web_server, daemon=True).start()    