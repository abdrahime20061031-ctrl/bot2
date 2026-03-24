import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. إعدادات البوت
TOKEN = '8507097163:AAFFUKzBzYLeE9HAgT-M-xj9SSkfRDu3Mjg'

LESSONS = {
    "logic": "https://drive.google.com/your-logic-link",
    "algo": "https://drive.google.com/your-algo-link",
    "structure": "https://drive.google.com/your-structure-link"
}

# 2. كود السيرفر الوهمي (لإبقاء Render مستيقظاً)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YCan Bot is Running Successfully!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"🌍 Web Server started on port {port}")
    server.serve_forever()

# 3. دوال البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📐 دروس المنطق التعاقبي", callback_query_data='logic')],
        [InlineKeyboardButton("💻 خوارزميات ومخططات", callback_query_data='algo')],
        [InlineKeyboardButton("🏗️ هندسة الحاسوب", callback_query_data='structure')],
        [InlineKeyboardButton("👨‍💻 المطور: YCan", url='https://instagram.com/mansouri_abderrahime')] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"مرحباً {update.effective_user.first_name} في مساعد MI L1!\nاختر الدرس المطلوبة:",
        reply_markup=reply_markup
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lesson_key = query.data
    if lesson_key in LESSONS:
        link = LESSONS[lesson_key]
        message = f"✅ إليك الرابط المطلوب:\n{link}\n\n🤖 مبرمج بواسطة: Abderahime Mansouri"
        await query.edit_message_text(text=message)

# 4. تشغيل كل شيء
def main():
    # تشغيل السيرفر الوهمي في خيط (Thread) منفصل لكي لا يعطل البوت
    threading.Thread(target=run_web_server, daemon=True).start()

    # تشغيل البوت
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    print("🚀 البوت يعمل الآن.. اذهب وجربه!")
    app.run_polling()

if __name__ == '__main__':
    main()
