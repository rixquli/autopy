import platform
import sys

if platform.system() == 'Windows':
    import msvcrt
else:
    import termios
    import tty

def clear_input_buffer():
    if platform.system() == 'Windows':
        # Windows implementation
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        # Unix/Linux implementation
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

def safe_input(prompt=""):
    clear_input_buffer()  # Vide le buffer avant de demander l'entrée
    return input(prompt)