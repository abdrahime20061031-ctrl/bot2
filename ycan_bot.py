import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# 1. إعدادات البوت والدروس
# ==========================================
# تأكد من إضافة BOT_TOKEN في Environment Variables في Render
TOKEN = os.environ.get("8507097163:AAFFUKzBzYLeE9HAgT-M-xj9SSkfRDu3Mjg") 

LESSONS = {
    "logic": {
        "title": "📐 دروس المنطق التعاقبي",
        "link": "https://drive.google.com/your-logic-link"
    },
    "algo": {
        "title": "💻 الخوارزميات",
        "link": "https://drive.google.com/your-algo-link"
    },
    "structure": {
        "title": "🏗️ هندسة الحاسوب",
        "link": "https://drive.google.com/your-structure-link"
    }
}

# ==========================================
# 2. سيرفر Render (لحل مشكلة No open ports)
# ==========================================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YCan Bot is Alive and Running!")
    def log_message(self, format, *args): return # لتقليل الرسائل في الـ Logs

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"🌍 Web server started on port {port}")
    server.serve_forever()

# ==========================================
# 3. واجهات القوائم
# ==========================================
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📐 المنطق التعاقبي", callback_query_data='logic')],
        [InlineKeyboardButton("💻 الخوارزميات", callback_query_data='algo')],
        [InlineKeyboardButton("🏗️ هندسة الحاسوب", callback_query_data='structure')],
        [InlineKeyboardButton("👨‍💻 المطور", url="https://instagram.com/mansouri_abderrahime")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع للقائمة", callback_query_data='back')]])

# ==========================================
# 4. الأوامر ومعالجة الأزرار
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"✨ أهلاً {user.first_name} ✨\n\n🎓 مرحباً بك في بوت MI L1\n📚 اختر المادة المطلوبة:"
    await update.message.reply_text(text, reply_markup=main_menu())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back":
        await query.edit_message_text("📚 اختر المادة من القائمة:", reply_markup=main_menu())
        return

    if data in LESSONS:
        lesson = LESSONS[data]
        text = f"📌 {lesson['title']}\n\n🔗 رابط الدروس:\n{lesson['link']}\n\n🤖 مبرمج بواسطة: YCan"
        await query.edit_message_text(text=text, reply_markup=back_menu())

# ==========================================
# 5. دالة التشغيل الرئيسية
# ==========================================
def main():
    if not TOKEN:
        print("❌ Error: BOT_TOKEN not found!")
        return

    # تشغيل السيرفر الوهمي في خيط منفصل (مهم جداً لـ Render)
    threading.Thread(target=run_web_server, daemon=True).start()

    # تشغيل البوت
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("🚀 البوت انطلق بنجاح...")
    app.run_polling()

if __name__ == "__main__":
    main()
