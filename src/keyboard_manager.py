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

    def __del__(self):
        if self.listener:
            self.listener.stop()
