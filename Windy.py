import sys  # Ajoute cette importation en haut de ton fichier
import keyboard
import pyautogui
import win32gui
import win32con

def focus_window(title):
    # Simule la pression de touches shift
    pyautogui.PAUSE = 0  # Définis un délai très court entre les actions
    pyautogui.press('shift')
    
    # Trouver la fenêtre par le titre sans changer son état (ni restaurer, ni maximiser)
    def window_enum_handler(hwnd, top_windows):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            top_windows.append(hwnd)

    top_windows = []
    win32gui.EnumWindows(window_enum_handler, top_windows)
    
    if top_windows:
        hwnd = top_windows[0]
        win32gui.SetForegroundWindow(hwnd)  # Met simplement la fenêtre au premier plan
    else:
        print(f'Aucune fenêtre trouvée avec le titre : {title}')
stop = True
def on_key_event(event):
    key = event.name.upper()
    if key == 'ESC':  # Vérifie si la touche Échap a été pressée
        print("Arrêt du programme...")
        stop = False
        sys.exit(0)
    elif key in window_titles:
        focus_window(window_titles[key])

window_titles = {
    'F1': 'Fab-un - Dofus 2.71.3.4',
    'F2': 'Fab-deux - Dofus 2.71.3.4',
    'F3': 'Fab-three - Dofus 2.71.3.4',
    'F4': 'Fab-quattre - Dofus 2.71.3.4'
}

keyboard.on_press(on_key_event)

while stop:
    pass
