import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# 1. الإعدادات
# ==========================================
TOKEN = os.environ.get("8507097163:AAFFUKzBzYLeE9HAgT-M-xj9SSkfRDu3Mjg")

LESSONS = {
    "logic": {"title": "📐 دروس المنطق التعاقبي", "link": "https://drive.google.com/your-logic-link"},
    "algo": {"title": "💻 الخوارزميات", "link": "https://drive.google.com/your-algo-link"},
    "structure": {"title": "🏗️ هندسة الحاسوب", "link": "https://drive.google.com/your-structure-link"}
}

# ==========================================
# 2. سيرفر الويب (لإرضاء Render)
# ==========================================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YCan Bot is Alive!")
    def log_message(self, format, *args): return

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# ==========================================
# 3. معالجة الأزرار (التصحيح هنا)
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التصحيح: استخدم callback_data بدلاً من callback_query_data
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
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='back')]]))
    
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📐 المنطق التعاقبي", callback_data='logic')],
            [InlineKeyboardButton("💻 الخوارزميات", callback_data='algo')],
            [InlineKeyboardButton("🏗️ هندسة الحاسوب", callback_data='structure')],
            [InlineKeyboardButton("👨‍💻 المطور", url="https://instagram.com/mansouri_abderrahime")]
        ]
        await query.edit_message_text("📚 اختر المادة:", reply_markup=InlineKeyboardMarkup(keyboard))

# ==========================================
# 4. التشغيل
# ==========================================
def main():
    if not TOKEN: return
    
    # تشغيل السيرفر أولاً في الخلفية
    threading.Thread(target=run_web_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    print("🚀 البوت انطلق...")
    app.run_polling()

if __name__ == "__main__":
    main()
