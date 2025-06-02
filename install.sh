#!/bin/bash

# Make the script globally executable
chmod +x aid.py
ln -s  "$(pwd)/aid.py" /usr/bin/aid

# Function that takes a package name and installs it
install_package() {
if command -v dpkg &>/dev/null; then
        # Debian-based system
        if ! dpkg -s "$1" &>/dev/null; then
            echo "Installing $1"
            sudo apt-get update
            sudo apt-get install -y "$1"
        else
            echo "$1 is already installed."
        fi
    elif command -v rpm &>/dev/null; then
        # Redhat-based system
        if ! rpm -q "$1" &>/dev/null; then
            echo "Installing $1"
            sudo yum install -y "$1"
        else
            echo "$1 is already installed."
        fi
    else
        echo "Unsupported package manager. Please install $1 manually."
        exit 1
    fi
}

# TODO add all dependencies below
install_package python3
install_package python3-docopt
install_package python3-requests

# Populate the database
sudo -u postgres psql -d postgres -f init_data.sql
