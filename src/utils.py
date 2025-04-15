import msvcrt

def clear_input_buffer():
    # Vide le buffer d'entrée
    while msvcrt.kbhit():
        msvcrt.getch()

def safe_input(prompt=""):
    clear_input_buffer()  # Vide le buffer avant de demander l'entrée
    return input(prompt)