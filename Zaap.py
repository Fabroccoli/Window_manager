import keyboard
import pyautogui
import win32gui


# Définition des titres de fenêtre associés à chaque touche
window_titles = {
    'F1': 'Fab-un - Dofus 2.71.3.4',
    'F2': 'Fab-deux - Dofus 2.71.3.4',
    'F3': 'Fab-three - Dofus 2.71.3.4',
    'F4': 'Fab-quattre - Dofus 2.71.3.4'
}

# Fonction pour activer une fenêtre donnée
def activate_window(title):
    # Simule la pression de la touche Shift rapidement
    pyautogui.press('shift')

    # Trouver et activer la fenêtre par le titre
    def window_enum_handler(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
    hwnds = []
    win32gui.EnumWindows(window_enum_handler, hwnds)
    if hwnds:
        win32gui.SetForegroundWindow(hwnds[0])
    else:
        print(f'Aucune fenêtre trouvée avec le titre : {title}')

# Configuration des écouteurs de touches
for key in window_titles:
    keyboard.add_hotkey(key.lower(), activate_window, args=(window_titles[key],))

# Boucle pour garder le script en écoute continue
keyboard.wait('F12')  # Utilise la touche 'esc' pour quitter le script
