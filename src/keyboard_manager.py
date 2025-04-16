import platform
import keyboard
from pynput import keyboard as pynput_keyboard

class KeyboardManager:
    def __init__(self):
        self.system = platform.system()
        self.listener = None
        if self.system == "Linux":
            self.listener = pynput_keyboard.Listener(on_press=self._on_press)
            self.listener.start()
            self.pressed_keys = set()

    def _on_press(self, key):
        try:
            self.pressed_keys.add(key.char)
        except AttributeError:
            self.pressed_keys.add(str(key))

    def is_pressed(self, key):
        if self.system == "Windows":
            return keyboard.is_pressed(key)
        elif self.system == "Linux":
            return key in self.pressed_keys
        return False

    def press_and_release(self, keys):
        if self.system == "Windows":
            keyboard.press_and_release(keys)
        elif self.system == "Linux":
            key_combination = keys.split('+')
            with pynput_keyboard.Controller() as controller:
                for key in key_combination:
                    controller.press(key)
                for key in reversed(key_combination):
                    controller.release(key)

    def __del__(self):
        if self.listener:
            self.listener.stop()
