import platform
if platform.system() == "Linux":
    from pynput import keyboard as pynput_keyboard
    from threading import Event, Lock
import keyboard

class KeyboardManager:
    def __init__(self):
        self.system = platform.system()
        self.listener = None
        self.lock = Lock() if self.system == "Linux" else None
        self.pressed_keys = set()
        if self.system == "Linux":
            self._setup_listener()

    def _setup_listener(self):
        with self.lock:
            if self.listener:
                self.listener.stop()
            self.listener = pynput_keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
            self.listener.start()

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
        self._setup_listener()

    def is_pressed(self, key):
        if self.system == "Windows":
            return keyboard.is_pressed(key)
        elif self.system == "Linux":
            is_pressed = key in self.pressed_keys
            if is_pressed:
                self.resest_pressed_keys()
            return is_pressed
        return False
    
    def get_pressed_keys(self):
        if self.system == "Windows":
            keys = keyboard.get_hotkey_name()
            if keys:
                return keys
            return None
        elif self.system == "Linux":
            pressed_keys = set()
            key_combination = None
            key_event = Event()
            temp_listener = None

            def local_on_press(key):
                try:
                    pressed_keys.add(key.char)
                except AttributeError:
                    pressed_keys.add(str(key))

            def local_on_release(key):
                nonlocal key_combination
                key_strings = []
                for k in pressed_keys:
                    key_strings.append(str(k).replace("'", "").replace("Key.", ""))
                key_combination = keyboard.get_hotkey_name(key_strings)
                key_event.set()
                return False  # Stop listener

            try:
                temp_listener = pynput_keyboard.Listener(
                    on_press=local_on_press,
                    on_release=local_on_release,
                    suppress=False
                )
                temp_listener.start()
                key_event.wait(timeout=2)  # Réduit le timeout à 2 secondes
                return key_combination
            finally:
                if temp_listener and temp_listener.is_alive():
                    temp_listener.stop()
        return None

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
        if self.system == "Linux" and self.listener:
            try:
                self.listener.stop()
            except:
                pass