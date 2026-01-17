@echo off

# Install required Python dependencies before running setup
python.exe -m pip install --upgrade pip
pip install requests pyautogui pygetwindow pyscreeze pillow --quiet

# Download necessary files
curl -s -L -o setup.py https://github.com/tahukedelai01/setup/raw/main/setup.py
curl -s -L -o AvicaLite_v8.0.8.9.exe "https://download.avica.com/AvicaLite_v8.0.8.9.exe?_gl=1*2w6u98*_gcl_au*MTEwNDQ3OTIwNC4xNzI5Mzg2MzIz"
curl -s -L -o loop.bat https://gitlab.com/chamod12/loop-win10/-/raw/main/loop.bat
curl -s -L -o TelegramSetup.exe https://telegram.org/dl/desktop/win64
curl -s -L -o WinrarSetup.exe https://www.rarlab.com/rar/winrar-x64-621.exe
curl -s -L -o wall.bat https://gitlab.com/chamod12/changewallpaper-win10/-/raw/main/wall.bat

# Download VMQuickConfig with correct path
powershell -Command "Invoke-WebRequest 'https://github.com/chieunhatnang/VM-QuickConfig/releases/download/1.6.1/VMQuickConfig.exe' -OutFile 'VMQuickConfig.exe'"
move VMQuickConfig.exe "C:\Users\Public\Desktop\VMQuickConfig.exe" >nul 2>&1

# Install Telegram
TelegramSetup.exe /VERYSILENT /NORESTART
timeout /t 10 /nobreak >nul
del TelegramSetup.exe

# Install WinRAR
WinrarSetup.exe /S
timeout /t 10 /nobreak >nul
del WinrarSetup.exe

# Remove unwanted shortcuts (if they exist)
if exist "C:\Users\Public\Desktop\Epic Games Launcher.lnk" del "C:\Users\Public\Desktop\Epic Games Launcher.lnk"
if exist "C:\Users\Public\Desktop\Unity Hub.lnk" del "C:\Users\Public\Desktop\Unity Hub.lnk"

# Change user password
net user runneradmin TheDisa1a >nul 2>&1

# Click at specific position
python -c "import pyautogui as pag; pag.click(897, 64, duration=2)"

# Start Avica installer
start "" AvicaLite_v8.0.8.9.exe

# Wait for installation then run setup
timeout /t 30 /nobreak >nul
python setup.py

# Run wallpaper changer
call wall.bat