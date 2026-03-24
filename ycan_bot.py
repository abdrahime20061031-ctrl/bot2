import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# 1. الإعدادات (تم وضع التوكن هنا مباشرة)
# ==========================================
# تم استبدال os.environ بالتوكن الخاص بك مباشرة
TOKEN = "8507097163:AAFFUKzBzYLeE9HAgT-M-xj9SSkfRDu3Mjg"

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
# 2. سيرفر الويب (لحل مشكلة Port scan timeout في Render)
# ==========================================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YCan Bot is Running Successfully!")
    def log_message(self, format, *args): return

def run_web_server():
    # Render يطلب بورت معين، نأخذه من النظام أو نستخدم 10000 كافتراضي
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
    
    # التعامل مع كل من الرسائل الجديدة وتعديلات الأزرار
    text = f"أهلاً {update.effective_user.first_name} ✨\nاختر المادة من القائمة:"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data

    if data == "back":
        await start(update, context)
        return

    if data in LESSONS:
        lesson = LESSONS[data]
        text = f"📌 {lesson['title']}\n\n🔗 رابط الدروس:\n{lesson['link']}\n\n🤖 مبرمج بواسطة: YCan"
        back_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='back')]])
        await query.edit_message_text(text=text, reply_markup=back_button)

# ==========================================
# 4. التشغيل الرئيسي
# ==========================================
def main():
    # تشغيل سيرفر الويب في الخلفية أولاً (Thread)
    threading.Thread(target=run_web_server, daemon=True).start()

    # بناء البوت باستخدام التوكن
    app = Application.builder().token(TOKEN).build()

    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("🚀 البوت انطلق بنجاح... اذهب لتجربته!")
    app.run_polling()

if __name__ == "__main__":
    main()
