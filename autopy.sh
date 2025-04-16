#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please run installer.sh first."
    read -n 1 -s -r -p "Press any key to continue..."
    exit 1
fi

# Run the main program
python3 "$(dirname "$0")/main.py"
if [ $? -ne 0 ]; then
    echo "An error occurred while running the program."
    read -n 1 -s -r -p "Press any key to continue..."
    exit 1
fi

read -n 1 -s -r -p "Press any key to continue..."
