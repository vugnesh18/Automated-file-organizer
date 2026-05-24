#!/bin/bash

# Automated File Organizer - Linux/macOS Launcher
# This script helps you run the file organizer on Unix-like systems

echo ""
echo "======================================"
echo " Automated File Organizer - Launcher"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ using:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    exit 1
fi

# Run the CLI with interactive mode
python3 cli.py --interactive
