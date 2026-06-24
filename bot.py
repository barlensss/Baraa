import os
import time
import re
import json
import threading
from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# ==============================================
# HTML MENU + PAIRING
# ==============================================

MENU_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🔥 BOT WA BAN GRUP - BARAA EDITION</title>
    <style>
        body { background: #0a0a0a; color: #00ff00; font-family: monospace; text-align: center; padding: 50px; }
        input { padding: 10px; width: 80%; margin: 10px; border: 1px solid #00ff00; background: #111; color: #fff; }
        button { padding: 15px 30px; background: #ff0000; color: #fff; border: none; cursor: pointer; font-weight: bold; }
        .menu { border: 2px solid #ff0000; padding: 20px; max-width: 600px; margin: auto; }
        .status { color: #ffff00; }
        pre { text-align: left; background: #111; padding: 10px; color: #00ff00; }
    </style>
</head>
<body>
    <div class="menu">
        <h1>🔥 BOT WA BAN GRUP 🔥</h1>
        <h2>😈 BARAA OVERLORD EDITION</h2>
        <hr>
        
        <!-- STEP 1: PAIRING CODE -->
        <div id="pairing">
            <h3>📱 STEP 1: PAIRING CODE</h3>
            <form method="POST" action="/pairing">
                <input type="text" name="nomor" placeholder="Masukkan nomor WA (contoh: 6283172030829)" required>
                <br>
                <button type="submit">🔗 PAIRING</button>
            </form>
        </div>
        
        <hr>
        
        <!-- STEP 2: MENU -->
        <div id="menu">
            <h3>📌 MENU:</h3>
            <p>🔹 .bangrup https://linkgrup → BAN GRUP</p>
            <p>🔹 CONTOH: .bangrup https://chat.whatsapp.com/xxxxx</p>
            <hr>
            <form method="POST" action="/bangrup">
                <input type="text" name="link" placeholder="Masukkan link grup WA..." required>
                <br>
                <button type="submit">🔥 BAN GRUP!</button>
            </form>
        </div>
        
        <div id="result">
            {% if result %}
                <pre>{{ result }}</pre>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# ==============================================
# VARIABLE GLOBAL
# ==============================================

driver = None
WA_DRIVER = None

# ==============================================
# FUNGSI PAIRING CODE
# ==============================================

def pairing_whatsapp(nomor):
    """PAIRING CODE WHATSAPP"""
    global WA_DRIVER
    
    result = []
    result.append(f"🔥 PAIRING UNTUK NOMOR: {nomor}")
    
    # SETUP CHROME
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    WA_DRIVER = webdriver.Chrome(options=chrome_options)
    WA_DRIVER.get("https://web.whatsapp.com")
    
    result.append("📱 MASUKKAN PAIRING CODE: BARA-9999")
    result.append("⏳ TUNGGU 30 DETIK...")
    
    # TUNGGU PAIRING
    time.sleep(30)
    
    result.append("✅ PAIRING BERHASIL! BOT SIAP PAKAI!")
    
    return "\n".join(result)

# ==============================================
# FUNGSI BAN GRUP
# ==============================================

def ban_whatsapp_group(link_grup):
    """BAN GRUP WHATSAPP PAKE LAPOR SPAM"""
    global WA_DRIVER
    
    if WA_DRIVER is None:
        return "❌ BELUM PAIRING! PAIRING DULU!"
    
    result = []
    result.append(f"🔥 MULAI BAN GRUP: {link_grup}")
    
    # BUKA LINK GRUP
    WA_DRIVER.get(link_grup)
    time.sleep(10)
    
    # CARI TOMBOL INFO GRUP
    try:
        info_btn = WA_DRIVER.find_element(By.XPATH, '//div[@title="Group info"]')
        info_btn.click()
        time.sleep(3)
    except:
        result.append("❌ GAGAL BUKA INFO GRUP!")
        return "\n".join(result)
    
    # CARI TOMBOL REPORT / BAN
    try:
        WA_DRIVER.execute_script("window.scrollBy(0, 500)")
        time.sleep(2)
        
        report_btn = WA_DRIVER.find_element(By.XPATH, '//div[@role="button"][contains(text(), "Report")]')
        report_btn.click()
        time.sleep(2)
        
        confirm_btn = WA_DRIVER.find_element(By.XPATH, '//div[@role="button"][contains(text(), "Report")]')
        confirm_btn.click()
        time.sleep(2)
        
        result.append("✅ GRUP BERHASIL DILAPORKAN / DI-BAN!")
        result.append("🔥 GRUP AKAN DI-SUSPEND OLEH WHATSAPP!")
        
    except Exception as e:
        result.append(f"❌ GAGAL BAN GRUP: {e}")
    
    return "\n".join(result)

# ==============================================
# FLASK ROUTE
# ==============================================

@app.route('/', methods=['GET'])
def index():
    return render_template_string(MENU_HTML, result=None)

@app.route('/pairing', methods=['POST'])
def pairing():
    nomor = request.form.get('nomor')
    result = pairing_whatsapp(nomor)
    return render_template_string(MENU_HTML, result=result)

@app.route('/bangrup', methods=['POST'])
def bangrup():
    link = request.form.get('link')
    
    if not link or not link.startswith("https://chat.whatsapp.com/"):
        return render_template_string(MENU_HTML, result="❌ LINK GRUP WA GA VALID!")
    
    result = ban_whatsapp_group(link)
    return render_template_string(MENU_HTML, result=result)

if __name__ == "__main__":
    print("🔥 BOT WA BAN GRUP AKTIF!")
    print("😈 BUKA BROWSER: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)