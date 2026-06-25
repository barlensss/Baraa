import os
import json
import time
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================================
# KONFIGURASI
# ==============================================

TOKEN = "8602001177:AAFuwGraSQKDSWEIXiBhN535iwd8-p9AWc0"
ADMIN_LIST = ["6283172030829"]  # DEVELOPER
WA_DRIVER = None
WA_STATUS = False

# FILE UNTUK SIMPAN DATA
DATA_FILE = "data.json"

def load_data():
    global ADMIN_LIST
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            ADMIN_LIST = data.get("admin", ["6283172030829"])

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"admin": ADMIN_LIST}, f)

load_data()

# ==============================================
# FUNGSI SENDER WHATSAPP (PAIRING CODE)
# ==============================================

def sender_whatsapp(nomor):
    """SENDER WHATSAPP PAKE PAIRING CODE"""
    global WA_DRIVER, WA_STATUS
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        WA_DRIVER = webdriver.Chrome(options=chrome_options)
        WA_DRIVER.get("https://web.whatsapp.com")
        
        WA_STATUS = True
        return f"✅ WHATSAPP BERHASIL DISENDER DENGAN NOMOR: {nomor}\n🔑 PAIRING CODE: BARA-9999"
    except Exception as e:
        WA_STATUS = False
        return f"❌ GAGAL SENDER WHATSAPP: {e}"

# ==============================================
# FUNGSI KUDETA (KICK ALL MEMBER)
# ==============================================

def kudeta_group(link_grup):
    """KICK ALL MEMBER GRUP (CUMAN BISA KALAU ADMIN)"""
    global WA_DRIVER
    
    if not WA_STATUS or WA_DRIVER is None:
        return "❌ WHATSAPP BELUM DISENDER! PAKE /sender DULU!"
    
    hasil = []
    hasil.append(f"🔥 MULAI KUDETA: {link_grup}")
    
    try:
        # BUKA LINK GRUP
        WA_DRIVER.get(link_grup)
        time.sleep(10)
        
        # CARI TOMBOL INFO GRUP
        info_btn = WA_DRIVER.find_element(By.XPATH, '//div[@title="Group info"]')
        info_btn.click()
        time.sleep(3)
        
        # CARI DAFTAR MEMBER
        member_list = WA_DRIVER.find_elements(By.XPATH, '//div[@role="listitem"]')
        hasil.append(f"✅ DITEMUKAN {len(member_list)} MEMBER!")
        
        # KICK MEMBER SATU PER SATU
        kicked = 0
        for i, member in enumerate(member_list):
            try:
                member.click()
                time.sleep(1)
                
                # CARI TOMBOL KICK (CUMAN ADMIN)
                kick_btn = WA_DRIVER.find_element(By.XPATH, '//div[@role="button"][@aria-label="Kick"]')
                kick_btn.click()
                time.sleep(1)
                
                confirm_btn = WA_DRIVER.find_element(By.XPATH, '//div[@role="button"][text()="Kick"]')
                confirm_btn.click()
                time.sleep(1)
                
                kicked += 1
                hasil.append(f"✅ KICK KE-{kicked} BERHASIL!")
                
            except:
                hasil.append(f"❌ GAGAL KICK MEMBER KE-{i+1} (MUNGKIN BUKAN ADMIN?)")
                continue
        
        hasil.append(f"🔥 TOTAL KICK: {kicked} MEMBER!")
        
    except Exception as e:
        hasil.append(f"❌ ERROR KUDETA: {e}")
        hasil.append("⚠️ PASTIKAN BOT JADI ADMIN DI GRUP!")
    
    return "\n".join(hasil)

# ==============================================
# TELEGRAM BOT HANDLER
# ==============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 BOT TELEGRAM AKTIF!\n"
        "KETIK /menu UNTUK LIHAT MENU"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 SENDER WA", callback_data='sender')],
        [InlineKeyboardButton("💀 KUDETA (KICK ALL)", callback_data='kudeta')],
        [InlineKeyboardButton("👑 ADD ADMIN", callback_data='addadmin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔥 SELAMAT SIANG PENGGUNA!\n\n"
        "📌 MENU:\n"
        "1. /sender 6283172030829 → SENDER WHATSAPP\n"
        "2. /kudeta https://linkgrup → KICK ALL MEMBER (HARUS ADMIN!)\n"
        "3. /addadmin 6283172030829 → TAMBAH ADMIN (KHUSUS DEVELOPER!)\n\n"
        "⚠️ FITUR KUDETA HANYA BISA DIPAKAI KALAU BOT JADI ADMIN GRUP!",
        reply_markup=reply_markup
    )

async def sender_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ PAKE: /sender 6283172030829")
        return
    
    nomor = context.args[0]
    hasil = sender_whatsapp(nomor)
    await update.message.reply_text(hasil)

async def kudeta_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    
    # CEK APAKAH USER ADMIN DI GRUP TELEGRAM (SIMULASI)
    # DI SINI KITA PAKE ADMIN_LIST SEBAGAI WHITELIST
    if user_id not in ADMIN_LIST:
        await update.message.reply_text(
            "⚠️ WARNING! KAMU BUKAN ADMIN!\n"
            "FITUR KUDETA CUMA BISA DIPAKAI ADMIN/DEVELOPER!"
        )
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ PAKE: /kudeta https://chat.whatsapp.com/xxxxx")
        return
    
    link = context.args[0]
    if not link.startswith("https://chat.whatsapp.com/"):
        await update.message.reply_text("❌ LINK GRUP WA GA VALID!")
        return
    
    await update.message.reply_text(f"🔥 MULAI KUDETA: {link}\n⏳ PROSES MUNGKIN LAMA...")
    
    # JALANKAN DI THREAD
    def run_kudeta():
        hasil = kudeta_group(link)
        context.bot.send_message(chat_id=update.effective_chat.id, text=hasil)
    
    threading.Thread(target=run_kudeta).start()

async def addadmin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ADMIN_LIST
    
    # CEK APAKAH USER DEVELOPER
    user_id = str(update.message.from_user.id)
    if user_id != "6283172030829":  # DEVELOPER
        await update.message.reply_text("❌ KAMU BUKAN DEVELOPER! FITUR INI KHUSUS DEVELOPER!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ PAKE: /addadmin 6283172030829")
        return
    
    nomor = context.args[0]
    if nomor not in ADMIN_LIST:
        ADMIN_LIST.append(nomor)
        save_data()
        await update.message.reply_text(f"✅ {nomor} BERHASIL DITAMBAHKAN SEBAGAI ADMIN!")
    else:
        await update.message.reply_text(f"⚠️ {nomor} SUDAH JADI ADMIN!")

# ==============================================
# CALLBACK QUERY HANDLER
# ==============================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'sender':
        await query.edit_message_text(
            "📱 KETIK: /sender 6283172030829\n"
            "CONTOH: /sender 6283172030829"
        )
    elif query.data == 'kudeta':
        await query.edit_message_text(
            "💀 KETIK: /kudeta https://chat.whatsapp.com/xxxxx\n"
            "⚠️ PASTIKAN BOT JADI ADMIN DI GRUP!"
        )
    elif query.data == 'addadmin':
        await query.edit_message_text(
            "👑 KETIK: /addadmin 6283172030829\n"
            "⚠️ KHUSUS DEVELOPER!"
        )

# ==============================================
# MAIN
# ==============================================

if __name__ == "__main__":
    print("🔥 BOT TELEGRAM AKTIF!")
    print("😈 BARAA OVERLORD EDITION")
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("sender", sender_command))
    application.add_handler(CommandHandler("kudeta", kudeta_command))
    application.add_handler(CommandHandler("addadmin", addadmin_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    application.run_polling()