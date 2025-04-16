import os
import keyboard
import time
from datetime import datetime
from PIL import ImageGrab
import platform

# Détection du système d'exploitation
if platform.system() == 'Windows':
    import win32clipboard
    import win32con
else:
    import pyperclip

from src.utils import safe_input
from src.terminal_utils import (
    print_title, print_success, print_error,
    print_info, print_warning, print_menu_option,print_main_title
)

SCREENSHOTS_DIR = "screenshots"

def setup_directories():
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)

def trigger_windows_screenshot():
    # Récupère la derniere image du presse-papier si disponible
    previous_image = None
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
            print("Image déjà dans le presse-papier.")
            previous_image = win32clipboard.GetClipboardData(win32con.CF_DIB)
    finally:
        win32clipboard.CloseClipboard()

    # Simule Win+Shift+S pour lancer l'outil de capture
    keyboard.press_and_release('windows+shift+s')
    
    # Attend que l'utilisateur fasse sa capture
    print("Faites votre sélection avec l'outil de capture Windows...")
    time.sleep(1)  # Attente pour l'ouverture de l'outil
    
    # Attend que l'image soit dans le presse-papier
    max_wait = 30  # Temps maximum d'attente en secondes
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            if check_clipboard_different_from_previous(previous_image):
                print("Capture détectée!")
                time.sleep(0.5)  # Petit délai pour s'assurer que l'image est bien copiée
                return True
        except:
            pass
        time.sleep(0.5)
    
    return False

def check_clipboard_different_from_previous(previous_image):
        if platform.system() == 'Windows':
            try:
                win32clipboard.OpenClipboard()
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
                    if(previous_image == None):
                        return True
                    current_image = win32clipboard.GetClipboardData(win32con.CF_DIB)
                    return current_image != previous_image
            finally:
                win32clipboard.CloseClipboard()
            return False
        elif platform.system() == 'Linux':
            # Pour Linux, utiliser pyperclip pour vérifier le presse-papier
            current_image = pyperclip.paste()
            if previous_image is None:
                return True
            return current_image != previous_image

def save_clipboard_image():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SCREENSHOTS_DIR}/capture_{timestamp}.png"
    
    try:
        image = ImageGrab.grabclipboard()
        if image:
            image.save(filename)
            print(f"Capture sauvegardée: {filename}")
            return filename
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return None
    
    return None

def capture_screenshot():
    if trigger_windows_screenshot():
        return save_clipboard_image()
    return None

def record_key_combination():
    print("Appuyez sur la combinaison de touches (ou ESC pour annuler)...")
    recorded_keys = set()
    
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == 'down':
            if event.name == 'esc':
                return None
            recorded_keys.add(event.name)
        elif event.event_type == 'up':
            if recorded_keys:
                # Convertir le set en string avec le format "key1+key2+key3"
                return '+'.join(recorded_keys)
            

def record_action():
    actions = []
    try:
        while True:
            print_main_title("Record")
            print_menu_option("1", "Capture new action")
            print_menu_option("2", "Type text")
            print_menu_option("3", "Press key combination")
            print_menu_option("4", "Execute command")
            print_menu_option("5", "Start another sequence")
            print_menu_option("9", "Finish recording")
            
            while True:
                if keyboard.is_pressed('9'):
                    time.sleep(0.01)
                    return actions
            
                if keyboard.is_pressed('1'):
                    time.sleep(0.01)
                    image_path = capture_screenshot()
                    delay = float(safe_input("Delay before action (seconds): "))
                    if image_path:
                        actions.append({
                            "action_type": "click",
                            "image_path": image_path,
                            "delay": delay
                        })
                        print_success(f"Click action recorded!")
                    break
                elif keyboard.is_pressed('2'):
                    time.sleep(0.01)
                    text = safe_input("Texte à taper: ")
                    delay = float(safe_input("Délai avant l'action (en secondes): "))
                    actions.append({
                        "action_type": "type",
                        "text": text,
                        "delay": delay
                    })
                    break
                elif keyboard.is_pressed('3'):
                    time.sleep(0.01)
                    pressed_keys = record_key_combination()
                    if pressed_keys is None:
                        print("Enregistrement annulé.")
                        break
                    delay = float(safe_input("Délai avant l'action (en secondes): "))
                    actions.append({
                        "action_type": "pressed_keys",
                        "pressed_keys": pressed_keys,
                        "delay": delay
                    })
                    break
                elif keyboard.is_pressed('4'):
                    time.sleep(0.01)
                    command = safe_input("Commande à exécuter: ")
                    delay = float(safe_input("Délai avant l'action (en secondes): "))
                    actions.append({
                        "action_type": "command",
                        "command": command,
                        "delay": delay
                    })
                    break
                elif keyboard.is_pressed('5'):
                    time.sleep(0.01)
                    sequence_name = safe_input("Nom de la séquence: ")
                    delay = float(safe_input("Délai avant l'action (en secondes): "))
                    if sequence_name:
                        actions.append({
                            "action_type": "start_sequence",
                            "sequence_to_start": sequence_name,
                            "delay": delay 
                        })
                        break
                    return actions
    except KeyboardInterrupt:
        print_warning("\nRecording interrupted")
        return actions
   

def main():
    setup_directories()
    print("Programme d'enregistrement d'actions")
    return record_action()

if __name__ == "__main__":
    main()
