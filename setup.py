import pyautogui as pag
import time
import requests
import os
import pygetwindow as gw
import subprocess
import sys
from PIL import ImageGrab  # Alternative for screenshot

# Konfigurasi Telegram Bot
TELEGRAM_BOT_TOKEN = "8702870038:AAGOvfoxAMUFreoWjRdQgCkBqlHr1Y5jMB8"  # Ganti dengan token bot Anda
TELEGRAM_CHAT_ID = "5504921604"      # Ganti dengan ID Telegram Anda

# Install missing dependency if needed
try:
    import pyscreeze
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyscreeze", "--quiet"])
    import pyscreeze

actions = [
    (516, 405, 4),  # Click Avica
    (50, 100, 1),   # Settings/menu
    (249, 203, 4),  # Connect RDP
    (249, 203, 4),  # Confirm connect
    (249, 203, 4),  # Extra click
    (249, 203, 4),  # Extra click
    (447, 286, 4),  # Launch Avica
]

time.sleep(15)

img_filename = 'AvicaRemoteIDFixed.png'

def send_photo_to_telegram(image_path, caption=""):
    """Send photo to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            result = response.json()
            if result.get('ok'):
                print(f"Foto berhasil dikirim ke Telegram: {caption}")
                return True
            else:
                print(f"Gagal mengirim ke Telegram: {result}")
                return False
    except Exception as e:
        print(f"Error mengirim ke Telegram: {e}")
        return False

def send_message_to_telegram(message):
    """Send text message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        if result.get('ok'):
            print(f"Pesan berhasil dikirim ke Telegram: {message[:50]}...")
            return True
        else:
            print(f"Gagal mengirim pesan: {result}")
            return False
    except Exception as e:
        print(f"Error mengirim pesan: {e}")
        return False

def minimize_non_avica():
    """Minimize semua window kecuali Avica"""
    for w in gw.getAllWindows():
        try:
            title = w.title.lower()
            if "avica" not in title and not w.isMinimized:
                w.minimize()
        except:
            pass

def take_screenshot():
    """Take screenshot with fallback methods"""
    try:
        # Try pyautogui first
        pag.screenshot().save(img_filename)
        return True
    except Exception as e:
        print(f"PyAutoGUI screenshot failed: {e}")
        try:
            # Try PIL alternative
            screenshot = ImageGrab.grab()
            screenshot.save(img_filename)
            return True
        except Exception as e2:
            print(f"PIL screenshot failed: {e2}")
            # Create a simple text file as fallback
            with open(img_filename, 'w') as f:
                f.write("Screenshot failed. Avica Remote ID placeholder.")
            return False

def main():
    # Kirim notifikasi awal
    send_message_to_telegram("🤖 Script Avica Remote dimulai...")
    
    for x, y, duration in actions:
        pag.click(x, y, duration=duration)
        
        # Handle connect to RDP
        if (x, y) == (249, 203):
            time.sleep(3)
            pag.click(x, y, duration=duration)
        
        # Handle setelah launch Avica
        if (x, y) == (447, 286):
            # Run Avica with correct path and quotes
            avica_path = "C:\\Program Files (x86)\\Avica\\Avica.exe"
            if os.path.exists(avica_path):
                subprocess.Popen(f'"{avica_path}"', shell=True)
                send_message_to_telegram("✅ Avica berhasil dijalankan")
            else:
                print("Avica.exe tidak ditemukan, coba jalankan dari installer...")
                subprocess.Popen("AvicaLite_v8.0.8.9.exe", shell=True)
                send_message_to_telegram("⚠️ Menjalankan installer Avica...")
            
            time.sleep(15)
            pag.click(249, 203, duration=4)
            time.sleep(3)
            minimize_non_avica()
            time.sleep(10)
            
            # Screenshot dan kirim ke Telegram
            if take_screenshot():
                print("Screenshot berhasil diambil")
                # Kirim screenshot ke Telegram
                send_photo_to_telegram(img_filename, "📸 Avica Remote ID - Screenshot")
            else:
                print("Gagal mengambil screenshot")
                send_message_to_telegram("❌ Gagal mengambil screenshot Avica")
            
        time.sleep(10)
    
    print("Done! Script selesai dijalankan.")
    send_message_to_telegram("✅ Script Avica Remote selesai dijalankan!")
    
    # Keep script running untuk monitoring
    while True:
        time.sleep(60)
        # Optional: bisa ditambahkan monitoring lain jika diperlukan
        pass

if __name__ == "__main__":
    # Cek konfigurasi Telegram
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("⚠️ PERINGATAN: Silakan ganti TELEGRAM_BOT_TOKEN dan TELEGRAM_CHAT_ID dengan nilai yang benar!")
        print("Program akan tetap berjalan tapi tanpa notifikasi Telegram.")
    
    main()
