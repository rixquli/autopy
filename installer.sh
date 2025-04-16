#!/bin/bash

echo -e "\e[94m==============================================="
echo "              AutoPY Installer"
echo -e "===============================================\e[0m"

# Check if Python is installed
echo -e "\e[93mChecking Python installation...\e[0m"
if ! command -v python3 &> /dev/null; then
    echo -e "\e[91mPython is not installed. Installing Python...\e[0m"
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python python-pip
    else
        echo -e "\e[91mCould not detect package manager. Please install Python manually.\e[0m"
        exit 1
    fi
fi

# Install required packages
echo -e "\e[93mInstalling required packages...\e[0m"
python3 -m pip install --user -r "$(dirname "$0")/requirements.txt"

# Create desktop shortcut
echo -e "\e[92mCreating desktop shortcut...\e[0m"
DESKTOP_FILE="$HOME/Desktop/AutoPY.desktop"
cat > "$DESKTOP_FILE" << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=AutoPY
Comment=Python Automation Tool
Exec=bash "$(realpath "$(dirname "$0")/autopy.sh")"
Icon=$(realpath "$(dirname "$0")/assets/icon.ico")
Terminal=true
Categories=Development;
EOL

chmod +x "$DESKTOP_FILE"

# Add to PATH
echo -e "\e[92mAdding AutoPY to PATH...\e[0m"
SCRIPT_PATH="export PATH=\$PATH:$(realpath "$(dirname "$0")")"
if ! grep -q "$SCRIPT_PATH" "$HOME/.bashrc"; then
    echo "$SCRIPT_PATH" >> "$HOME/.bashrc"
fi

echo -e "\n\e[42;97m Installation complete! \e[0m"
echo -e "\e[92m-----------------------------------------------"
echo " You can now:"
echo " 1. Double click AutoPY shortcut on your desktop"
echo " 2. Type 'autopy.sh' in any terminal"
echo -e "-----------------------------------------------\e[0m"
echo "Please restart your terminal or run: source ~/.bashrc"
```
