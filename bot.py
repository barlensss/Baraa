import os
import json
import random
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")
PORT = int(os.environ.get("PORT", 8080))

STORAGE_FILE = "stikers.json"
STIKER_LIST = []

if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "r") as f:
        STIKER_LIST = json.load(f)

app = Flask(__name__)

@app.route('/')
def index():
    return "🔥 BARAA TIKTOK BOT AKTIF!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return 'ok'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 BARAA TIKTOK BOT AKTIF!\n\n"
        "/addstiker ID → TAMBAH STIKER\n"
        "/bug @user → SPAM STIKER\n"
        "/list → LIHAT STIKER"
    )

async def add_stiker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ PAKE: /addstiker STIKER_ID")
        return
    stiker_id = context.args[0]
    if stiker_id not in STIKER_LIST:
        STIKER_LIST.append(stiker_id)
        with open(STORAGE_FILE, "w") as f:
            json.dump(STIKER_LIST, f)
        await update.message.reply_text(f"✅ STIKER {stiker_id} TERSIMPAN!")
    else:
        await update.message.reply_text(f"⚠️ STIKER {stiker_id} UDAH ADA!")

async def list_stiker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not STIKER_LIST:
        await update.message.reply_text("❌ BELUM ADA STIKER! PAKE /addstiker DULU!")
        return
    await update.message.reply_text("📌 DAFTAR STIKER:\n" + "\n".join(STIKER_LIST))

async def bug_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ PAKE: /bug @username")
        return
    target = context.args[0].replace("@", "")
    if not STIKER_LIST:
        await update.message.reply_text("❌ BELUM ADA STIKER!")
        return
    await update.message.reply_text(f"🔥 SPAM KE @{target} DIMULAI!")
    for i in range(100):
        stiker = random.choice(STIKER_LIST)
        print(f"✅ STIKER KE-{i+1} TERKIRIM: {stiker}")
    await update.message.reply_text(f"✅ SPAM KE @{target} SELESAI!")

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addstiker", add_stiker))
    application.add_handler(CommandHandler("bug", bug_tiktok))
    application.add_handler(CommandHandler("list", list_stiker))
    app.run(host='0.0.0.0', port=PORT)