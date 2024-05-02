import keyboard
import pyautogui
import win32gui
import json

# Fonction pour charger une configuration depuis un fichier spécifique
def load_config(filename):
    try:
        with open(filename + '.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Fichier non trouvé.")
        return None

# Fonction pour sauvegarder la configuration dans un fichier spécifique
def save_config(window_titles, filename):
    with open(filename + '.json', 'w') as file:
        json.dump(window_titles, file, indent=4)
    print("Configuration sauvegardée avec succès dans", filename + '.json')

# Variable pour suivre si la configuration a été chargée
config_loaded = False

# Demander à l'utilisateur s'il souhaite charger une configuration existante
if input("Avez-vous une configuration à charger ? (oui/non) ").lower() == 'oui':
    filename = input("Entrez le nom du fichier à charger : ")
    window_titles = load_config(filename)
    if window_titles:
        print("Configuration chargée avec succès.")
        config_loaded = True
        for key, value in window_titles.items():
            print(f"{key}: {value}")
    else:
        window_titles = {}
else:
    window_titles = {}

# Si aucune configuration n'est chargée ou si l'utilisateur souhaite en créer une nouvelle
if not window_titles:
    total = int(input("Nombre de perso: "))
    for n in range(1, total + 1):
        nom = input(f"Entrer le nom du perso {n} (Attention aux majuscule) : ")
        touche = input(f"Entrer une touche pour {nom} : ")
        version = " - Dofus 2.71.4.5"
        window_titles[touche] = f'{nom}{version}'

# Demander à l'utilisateur s'il souhaite sauvegarder cette configuration, uniquement si aucune config n'a été chargée
if not config_loaded:
    do_save = input("Voulez-vous sauvegarder cette configuration ? (oui/non) ")
    if do_save.lower() == 'oui':
        filename = input("Entrez le nom du fichier pour sauvegarder : ")
        save_config(window_titles, filename)
    else:
        print("Sauvegarde non effectuée.")


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
