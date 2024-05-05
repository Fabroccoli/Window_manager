import eel
import keyboard
import pyautogui
import win32gui
import json
import os
import time
import ctypes

# Fonction pour masquer la fenêtre de la console
def hide_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)

# Masquer la console immédiatement
hide_console()

eel.init('web')  # Initialisation du répertoire contenant les ressources web

window_keys = {}
character_keys = {}  # Dictionnaire pour la sauvegarde

@eel.expose
def assign_keys_to_windows(characters):
    global window_keys
    global character_keys
    window_keys.clear()
    character_keys.clear()  # Préparer pour une nouvelle sauvegarde

    def enum_windows_callback(hwnd, extra):
        window_text = win32gui.GetWindowText(hwnd)
        for character in characters:
            if character['name'].lower() in window_text.lower():
                window_keys[hwnd] = character['key']
                character_keys[character['name']] = character['key']  # Sauvegarder par nom
                print(f"Window ID: {hwnd}, Window Name: {window_text}, Key assigned: {character['key']}")
                keyboard.add_hotkey(character['key'].lower(), activate_window, args=(hwnd,))

    win32gui.EnumWindows(enum_windows_callback, None)
    return window_keys  # Retourne le dictionnaire des affectations clés pour confirmation

@eel.expose
def save_keys_to_file(filename):
    config_path = 'config'  # Définir le nom du dossier de configuration
    if not os.path.exists(config_path):
        os.makedirs(config_path)  # Créer le dossier s'il n'existe pas

    full_path = os.path.join(config_path, f"{filename}.json")  # Construire le chemin complet du fichier
    with open(full_path, 'w') as file:
        json.dump(character_keys, file, indent=4)
    return f"Configuration saved successfully as {full_path}"

@eel.expose
def activate_window(hwnd):
    try:
        pyautogui.press('shift')
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"Failed to activate window: {e}")

eel.start('index.html', block = False)

while True:
    eel.sleep(1)