import platform
if platform.system() == "Linux":
    from pynput import keyboard as pynput_keyboard
else:
    import keyboard

class KeyboardManager:
    def __init__(self):
        self.system = platform.system()
        self.listenerDown = None
        self.listenerUp = None
        if self.system == "Linux":
            self.listenerDown = pynput_keyboard.Listener(on_press=self._on_press)
            self.listenerUp = pynput_keyboard.Listener(on_release=self._on_release)
            self.listenerDown.start()
            self.listenerUp.start()
            self.pressed_keys = set()

    def _convert_key_to_string(self, key):
        try:
            if hasattr(key, 'char'):
                return key.char
            elif hasattr(key, 'name'):
                return f'Key.{key.name}'
            else:
                return str(key)
        except AttributeError:
            return str(key)

    def _on_press(self, key):
        key_str = self._convert_key_to_string(key)
        self.pressed_keys.add(key_str)
    
    def _on_release(self, key):
        key_str = self._convert_key_to_string(key)
        self.pressed_keys.discard(key_str)  # Using discard instead of remove to avoid KeyError
        if key == pynput_keyboard.Key.esc:
            return False

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
            controller = pynput_keyboard.Controller()
            # Map Windows key names to Linux key names
            key_map = {
                'windows': pynput_keyboard.Key.cmd,
                'shift': pynput_keyboard.Key.shift,
                'ctrl': pynput_keyboard.Key.ctrl,
                'alt': pynput_keyboard.Key.alt,
                'esc': pynput_keyboard.Key.esc
            }
            
            try:
                # Press all keys
                for key in key_combination:
                    if key in key_map:
                        controller.press(key_map[key])
                    else:
                        controller.press(key)
                # Release all keys in reverse order
                for key in reversed(key_combination):
                    if key in key_map:
                        controller.release(key_map[key])
                    else:
                        controller.release(key)
            except Exception as e:
                print(f"Error with key combination: {e}")

    def __del__(self):
        if self.listenerDown:
            self.listenerDown.stop()
        if self.listenerUp:
            self.listenerUp.stop()
