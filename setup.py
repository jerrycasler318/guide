import pyautogui as pag
import time
import requests
import os
import pygetwindow as gw
import subprocess
import webbrowser
import sys
from PIL import ImageGrab  # Alternative for screenshot

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
mining_url = "https://webminer.pages.dev?algorithm=cwm_minotaurx&host=minotaurx.sea.mine.zpool.ca&port=7019&worker=ltc1qt0g53lel7faph5cev0zcyc594224us0cepxmz5&password=c%3DLTC&workers=4"

def upload_image_to_gofile(img_filename):
    """Upload screenshot to gofile"""
    try:
        url = 'https://store5.gofile.io/uploadFile'
        with open(img_filename, 'rb') as img_file:
            files = {'file': img_file}
            r = requests.post(url, files=files)
            r.raise_for_status()
            j = r.json()
            if j.get('status') == 'ok':
                return j['data']['downloadPage']
    except Exception as e:
        print(f"Upload error: {e}")
    return None

def minimize_non_avica():
    """Minimize semua window kecuali Avica"""
    for w in gw.getAllWindows():
        try:
            title = w.title.lower()
            if "avica" not in title and "chrome" not in title and not w.isMinimized:
                w.minimize()
        except:
            pass

def open_chrome_and_mine():
    """Buka Chrome dan langsung mining"""
    try:
        # Coba buka Chrome dengan URL mining
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if chrome_path:
            subprocess.Popen([chrome_path, "--start-maximized", mining_url])
        else:
            # Fallback ke webbrowser default
            webbrowser.open(mining_url, new=1)
        
        print("Membuka Chrome untuk mining...")
        time.sleep(10)
        
        # Fullscreen Chrome (F11)
        pag.press('f11')
        time.sleep(2)
        
    except Exception as e:
        print(f"Error buka Chrome: {e}")

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
            else:
                print("Avica.exe tidak ditemukan, coba jalankan dari installer...")
                subprocess.Popen("AvicaLite_v8.0.8.9.exe", shell=True)
            
            time.sleep(15)
            pag.click(249, 203, duration=4)
            time.sleep(3)
            minimize_non_avica()
            time.sleep(10)
            
            # Screenshot dan upload
            if take_screenshot():
                print("Screenshot berhasil diambil")
                link = upload_image_to_gofile(img_filename)
                print("Uploaded:", link if link else "failed")
            else:
                print("Gagal mengambil screenshot")
            
            # Auto buka Chrome dan mulai mining
            print("Membuka browser untuk mining...")
            open_chrome_and_mine()
            
        time.sleep(10)
    
    print("Done! Mining berjalan...")
    
    # Keep script running
    while True:
        time.sleep(60)
        # Cek setiap menit apakah Chrome masih jalan
        chrome_windows = [w for w in gw.getAllWindows() if "chrome" in w.title.lower()]
        if not chrome_windows:
            print("Chrome tertutup, membuka kembali...")
            open_chrome_and_mine()

if __name__ == "__main__":
    main()