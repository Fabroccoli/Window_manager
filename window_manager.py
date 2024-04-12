import pygetwindow as gw
import keyboard
import pyautogui

def focus_window(title):

    # Simule la pression de touches shift
    pyautogui.PAUSE = 0  # Définis un délai très court entre les actions
    pyautogui.press('shift')

    windows = gw.getWindowsWithTitle(title)
    if windows:
        window = windows[0]
        if not window.isActive:
            window.activate()
        else:
            print(f'La fenêtre "{title}" est déjà active.')
    else:
        print(f'Aucune fenêtre trouvée avec le titre : {title}')

def on_key_event(event):
    key = event.name.upper()
    if key in window_titles:
        focus_window(window_titles[key])

window_titles = {
    'F1': 'Fab-un - Dofus 2.71.3.4',
    'F2': 'Fab-deux - Dofus 2.71.3.4',
    'F3': 'Fab-three - Dofus 2.71.3.4',
    'F4': 'Fab-quattre - Dofus 2.71.3.4'
}

keyboard.on_press(on_key_event)

while True:
    pass