#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Pip
sudo apt install python3 python3-pip python3-venv -y

# Clone your repository (User should replace <repo-url>)
# git clone <your-repository-url>
# cd Ransomware-Project

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install flask gunicorn

# Setup Gunicorn (Production server)
# You can run it manually with:
# gunicorn --bind 0.0.0.0:5000 server:app

echo "VPS Setup complete. Run 'source .venv/bin/activate && gunicorn --bind 0.0.0.0:5000 server:app' to start the server."
