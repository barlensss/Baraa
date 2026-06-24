import os
import time
import json
import random
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# KONFIGURASI DARI ENVIRONMENT VARIABLES
TOKEN = os.environ.get("TELEGRAM_TOKEN")
PORT = int(os.environ.get("PORT", 8080))

# FILE STIKER
STORAGE_FILE = "stikers.json"
STIKER_LIST = []

if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "r") as f:
        STIKER_LIST = json.load(f)

# FLASK APP
app = Flask(__name__)

@app.route('/')
def index():
    return "🔥 BARAA TIKTOK BOT AKTIF!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return 'ok'

# ==============================================
# FUNGSI TELEGRAM BOT
# ==============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 BARAA TIKTOK BOT AKTIF!\n\n"
        "📌 COMMAND:\n"
        "/addstiker ID → TAMBAH STIKER\n"
        "/bug @user → SPAM STIKER\n"
        "/list → LIHAT STIKER\n"
        "/help → BANTUAN"
    )

async def add_stiker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ GUNAKAN: /addstiker STIKER_ID")
        return
    
    stiker_id = context.args[0]
    if stiker_id not in STIKER_LIST:
        STIKER_LIST.append(stiker_id)
        with open(STORAGE_FILE, "w") as f:
            json.dump(STIKER_LIST, f)
        await update.message.reply_text(f"✅ STIKER {stiker_id} BERHASIL DISIMPAN!")
    else:
        await update.message.reply_text(f"⚠️ STIKER {stiker_id} SUDAH ADA!")

async def list_stiker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not STIKER_LIST:
        await update.message.reply_text("❌ GA ADA STIKER! PAKE /addstiker DULU!")
        return
    
    msg = "📌 DAFTAR STIKER:\n" + "\n".join(STIKER_LIST)
    await update.message.reply_text(msg)

async def bug_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ GUNAKAN: /bug @username")
        return
    
    target = context.args[0].replace("@", "")
    
    if not STIKER_LIST:
        await update.message.reply_text("❌ GA ADA STIKER! PAKE /addstiker DULU!")
        return
    
    await update.message.reply_text(f"🔥 MULAI SPAM KE @{target}...")
    
    # JALANKAN SPAM DI THREAD
    threading.Thread(target=spam_stiker_simulasi, args=(target, 100)).start()
    
    await update.message.reply_text(f"✅ SPAM KE @{target} SEDANG BERJALAN!")

def spam_stiker_simulasi(target, count=100):
    """SIMULASI KIRIM STIKER (TAPI BISA DIUBAH PAKE SELENIUM)"""
    for i in range(count):
        stiker = random.choice(STIKER_LIST)
        print(f"✅ STIKER KE-{i+1} TERKIRIM KE @{target}: {stiker}")
        time.sleep(0.5)
    
    print(f"✅ SPAM KE @{target} SELESAI!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 BARAA TIKTOK BOT\n\n"
        "/start → MULAI BOT\n"
        "/addstiker ID → TAMBAH STIKER\n"
        "/bug @user → SPAM STIKER\n"
        "/list → LIHAT STIKER\n"
        "/help → BANTUAN"
    )

# ==============================================
# MAIN
# ==============================================

if __name__ == "__main__":
    # SETUP TELEGRAM BOT
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addstiker", add_stiker))
    application.add_handler(CommandHandler("bug", bug_tiktok))
    application.add_handler(CommandHandler("list", list_stiker))
    application.add_handler(CommandHandler("help", help_command))
    
    # FLASK WEBHOOK
    app.run(host='0.0.0.0', port=PORT)