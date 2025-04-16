from colorama import init, Fore, Back, Style
from alive_progress import alive_bar
import os
import time
from pyfiglet import Figlet

# Initialize colorama
init()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title(text):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {text} ==={Style.RESET_ALL}")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")

def print_warning(text):
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def print_menu_option(key, text):
    print(f"{Fore.YELLOW}{Style.BRIGHT}[{key}]{Style.RESET_ALL} {text}")

def print_banner(text, color=Fore.CYAN, font='slant'):
    f = Figlet(font=font)
    banner = f.renderText(text)
    print(f"{color}{Style.BRIGHT}{banner}{Style.RESET_ALL}")

def print_main_title(text):
    clear()
    print_banner(text)

IS_RUNNING = False

def show_startup_animation(duration=3):
    global IS_RUNNING
    IS_RUNNING = True
    print_banner("Starting AutoPY", color=Fore.GREEN)
    print_info("Ce chargement ne sert strictement à rien, mais c'est trop stylé !")
    with IS_RUNNING and alive_bar(100, title='Loading', bar='blocks', spinner='dots') as bar:
        for i in range(100):
            if not IS_RUNNING:
                clear()
                return
            time.sleep(duration/100)
            bar()
    clear()

def stop_startup_animation():
    print
    global IS_RUNNING
    IS_RUNNING = False