#!/bin/bash
# Fix PythonAnywhere virtualenv setup

echo "=== Fixing Virtualenv Setup ==="

# Navigate to project directory
cd ~/lightoflord.pythonanywhere.com

# Remove old virtualenv
echo "Removing old virtualenv..."
rm -rf venv

# Create new virtualenv
echo "Creating new virtualenv..."
virtualenv --python=python3 venv

# Activate virtualenv
echo "Activating virtualenv..."
source venv/bin/activate

# Install required packages
echo "Installing Flask packages..."
pip install flask flask-sqlalchemy flask-login werkzeug

# Check installation
echo "Checking installed packages..."
pip list

echo "=== Virtualenv Setup Complete ==="
echo "Now restart your web app in PythonAnywhere!"
