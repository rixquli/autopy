import platform
if platform.system() == "Linux":
  from pynput import keyboard as pynput_keyboard
else:
  import keyboard
class KeyboardManager:
    def __init__(self):
        self.system = platform.system()
        self.listener = None
        if self.system == "Linux":
            self.listener = pynput_keyboard.Listener(on_press=self._on_press,on_release=self._on_release)
            self.listener.start()
            self.pressed_keys = set()

    def _on_press(self, key):
        try:
            self.pressed_keys.add(key.char)
        except AttributeError:
            self.pressed_keys.add(str(key))
    
    def _on_release(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)
        
        try:
            self.pressed_keys.remove(key_str)
        except KeyError:
            # Key wasn't in the set, which is fine
            pass
            
        if key == pynput_keyboard.Key.esc:
            return False
        
    def pause_listener(self):
        if self.listener:
            self.listener.stop()

    def resume_listener(self):
        if self.listener:
            self.listener.start()

    def is_pressed(self, key):
        if self.system == "Windows":
            return keyboard.is_pressed(key)
        elif self.system == "Linux":
            is_pressed = key in self.pressed_keys
            if is_pressed:
                self.resest_pressed_keys()
            return is_pressed
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
    
    def resest_pressed_keys(self):
        if self.system == "Linux":
            self.pressed_keys = set()

    def __del__(self):
        if self.listener:
            self.listener.stop()