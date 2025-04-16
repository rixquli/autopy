import pyautogui
import time
import json
from dataclasses import dataclass
import keyboard
from typing import List, Dict, Literal
import ctypes
from src.action_recorder import main as action_recorder
from src.utils import safe_input
from src.terminal_utils import (
    print_title, print_success, print_error,
    print_info, print_warning, print_menu_option, clear, 
    print_main_title, show_startup_animation
)
import subprocess
import threading
from src.keyboard_manager import KeyboardManager

@dataclass
class Action:
    delay: float
    action_type: Literal["click", "type", "pressed_keys", "command", "start_sequence"]
    sequence_name: str
    image_path: str = ""
    text: str = ""  # Optional for type action
    pressed_keys: str = ""
    command: str = ""  # Optional for command action
    sequence_to_start: str = ""  # Optional for start_sequence action

keyboard_manager = KeyboardManager()
class SequenceManager:
    def __init__(self, json_file: str):
        self.json_file = json_file
        self.sequences: Dict[str, List[Action]] = {}
        self.load_sequences()

    def load_sequences(self):
        try:
            with open(self.json_file, 'r') as f:
                content = f.read()
                if not content:  # If file is empty
                    self.sequences = {}
                    self.save_sequences()  # Initialize with empty dict
                else:
                    data = json.loads(content)
                    for sequence_name, actions in data.items():
                        self.sequences[sequence_name] = [
                            Action(**action, sequence_name=sequence_name) 
                            for action in actions
                        ]
        except FileNotFoundError:
            self.sequences = {}
            self.save_sequences()  # Create file with empty dict
        except json.JSONDecodeError:
            print(f"Warning: {self.json_file} contains invalid JSON. Creating new empty file.")
            self.sequences = {}
            self.save_sequences()

    def save_sequences(self):
        data = {
            sequence_name: [
                {"image_path": action.image_path, "delay": action.delay, "action_type": action.action_type, "text": action.text, "pressed_keys": action.pressed_keys, "command": action.command, "sequence_to_start": action.sequence_to_start}
                for action in actions
            ]
            for sequence_name, actions in self.sequences.items()
        }
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def add_action(self, sequence_name: str, action):
        if sequence_name not in self.sequences:
            self.sequences[sequence_name] = []
        self.sequences[sequence_name].append(
            Action(**action, sequence_name=sequence_name)
        )
        self.save_sequences()

    def get_sequence(self, sequence_name: str) -> List[Action]:
        return self.sequences.get(sequence_name, [])

    def list_sequences(self) -> List[str]:
        return list(self.sequences.keys())

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
SPI_SETCURSORS = 0x0057
SPI_SETCURSORVIS = 0x0101

def hide_cursor():
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETCURSORVIS, 0, None, 0)

def show_cursor():
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETCURSORVIS, 1, None, 0)

def execute_sequence(sequence_manager: SequenceManager, sequence_name: str):
    actions = sequence_manager.get_sequence(sequence_name)
    for action in actions:
        print(f"Executing action: {action.action_type} with delay {action.delay} seconds")
        if(action.action_type == "click"):
            execute_click_sequence(action)
        elif(action.action_type == "type"):
            execute_type_sequence(action)
        elif(action.action_type == "pressed_keys"):
            execute_pressed_keys_sequence(action)
        elif(action.action_type == "command"):
            execute_command_sequence(action)
        elif(action.action_type == "start_sequence"):
            if(action.sequence_to_start in sequence_manager.sequences):
                # Crée un nouveau thread pour exécuter la séquence
                thread = threading.Thread(
                    target=execute_sequence,
                    args=(sequence_manager, action.sequence_to_start)
                )
                thread.start()
                # Si vous voulez attendre que le thread termine avant de continuer
                # thread.join()

def execute_click_sequence(action: Action):
    time.sleep(action.delay)
    try:
        location = pyautogui.locateOnScreen(action.image_path, confidence=0.8)
        if location:
            pyautogui.click(location)
            print(f"Clicked on {action.image_path}")
        else:
            print(f"Image {action.image_path} not found")
    except Exception as e:
        print(f"Error executing action: {e}")
    show_cursor()

def execute_type_sequence(action: Action):
    time.sleep(action.delay)
    try:
        pyautogui.typewrite(action.text, interval=0.1)
        print(f"Typed text: {action.text}")
    except Exception as e:
        print(f"Error executing action: {e}")

def execute_pressed_keys_sequence(action: Action):
    time.sleep(action.delay)
    try:
        
        keyboard_manager.press_and_release(action.pressed_keys)
        print(f"Pressed keys: {action.pressed_keys}")
    except Exception as e:
        print(f"Error executing action: {e}")

def execute_command_sequence(action: Action):
    time.sleep(action.delay)
    try:
        # Execute the command using subprocess or os.system
        subprocess.run(action.command, shell=True)
        print(f"Executed command: {action.command}")
    except Exception as e:
        print(f"Error executing action: {e}")

def main():
    sequence_manager = SequenceManager('sequences.json')
    try:
        show_startup_animation()  # Ajouter l'animation de démarrage
        while True:
            print_main_title("AutoPY")
            
            if sequence_manager.list_sequences():
                print_info("Available sequences:")
                for seq in sequence_manager.list_sequences():
                    print(f"  • {seq}")
            else:
                print_warning("No sequences available")

            print_title("Menu")
            print_menu_option("1", "Execute sequence")
            print_menu_option("2", "Create new sequence")
            print_menu_option("3", "Add action to sequence")
            print_menu_option("9", "Exit")
            
            while True:
                if keyboard_manager.is_pressed('9'):
                    time.sleep(0.01)
                    print_info("Exiting...")
                    return
                
                if keyboard_manager.is_pressed('1'):
                    time.sleep(0.01)
                    sequence_name = safe_input("Enter sequence name: ")
                    if sequence_name in sequence_manager.sequences:
                        execute_sequence(sequence_manager, sequence_name)
                        print_success(f"Sequence '{sequence_name}' executed successfully!")
                    else:
                        print_error("Sequence not found!")
                    break
                
                elif keyboard_manager.is_pressed('2'):
                    time.sleep(0.01)
                    sequence_name = safe_input("Enter new sequence name: ")
                    sequences = action_recorder()
                    for action in sequences:
                        sequence_manager.add_action(sequence_name, action)
                    print_success("Sequence created!")
                    break
                
                elif keyboard_manager.is_pressed('3'):
                    time.sleep(0.01)
                    sequence_name = safe_input("Enter existing sequence name: ")
                    if sequence_name in sequence_manager.sequences:
                        sequences = action_recorder()
                        for action in sequences:
                            sequence_manager.add_action(sequence_name, action)
                        print_success("Actions added!")
                    else:
                        print_error("Sequence not found!")
                    break
    except KeyboardInterrupt:
        print_warning("Program interrupted. Exiting...")
            

if __name__ == "__main__":
    main()
