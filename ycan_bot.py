import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# 1. إعدادات البوت (التوكن والدروس)
# ==========================================
TOKEN = os.environ.get("8507097163:AAFFUKzBzYLeE9HAgT-M-xj9SSkfRDu3Mjg") 

LESSONS = {
    "logic": {"title": "📐 دروس المنطق التعاقبي", "link": "https://drive.google.com/your-logic-link"},
    "algo": {"title": "💻 الخوارزميات", "link": "https://drive.google.com/your-algo-link"},
    "structure": {"title": "🏗️ هندسة الحاسوب", "link": "https://drive.google.com/your-structure-link"}
}

# ==========================================
# 2. كود السيرفر (لحل مشكلة Timed Out في Render)
# ==========================================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YCan Bot is Alive!")
    def log_message(self, format, *args): return # لتقليل الرسائل في الـ Logs

def run_web_server():
    # Render يستخدم المنفذ 10000 أو ما يحدده في PORT
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"🌍 Web server started on port {port}")
    server.serve_forever()

# ==========================================
# 3. وظائف البوت
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📐 المنطق التعاقبي", callback_data='logic')],
        [InlineKeyboardButton("💻 الخوارزميات", callback_data='algo')],
        [InlineKeyboardButton("🏗️ هندسة الحاسوب", callback_data='structure')],
        [InlineKeyboardButton("👨‍💻 المطور", url="https://instagram.com/mansouri_abderrahime")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"أهلاً {update.effective_user.first_name} ✨\nاختر المادة:", reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data in LESSONS:
        lesson = LESSONS[query.data]
        text = f"📌 {lesson['title']}\n🔗 الرابط: {lesson['link']}"
        # زر الرجوع للقائمة الرئيسية
        back_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='back')]])
        await query.edit_message_text(text=text, reply_markup=back_button)
    
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📐 المنطق التعاقبي", callback_data='logic')],
            [InlineKeyboardButton("💻 الخوارزميات", callback_data='algo')],
            [InlineKeyboardButton("🏗️ هندسة الحاسوب", callback_data='structure')],
            [InlineKeyboardButton("👨‍💻 المطور", url="https://instagram.com/mansouri_abderrahime")]
        ]
        await query.edit_message_text("📚 اختر المادة من القائمة:", reply_markup=InlineKeyboardMarkup(keyboard))

# ==========================================
# 4. تشغيل كل شيء
# ==========================================
def main():
    if not TOKEN:
        print("❌ BOT_TOKEN not found!")
        return

    # تشغيل سيرفر الويب في خيط (Thread) منفصل لكي لا يتوقف البوت
    threading.Thread(target=run_web_server, daemon=True).start()

    # بناء وتشغيل البوت
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    print("🚀 البوت انطلق بنجاح...")
    app.run_polling()

if __name__ == "__main__":
    main()
