# Ransomware Simulation Project (Educational Case Study)

This project is an educational simulation designed for cybersecurity analysis and awareness. It demonstrates how ransomware-style software behaves in a controlled environment.

## ⚠️ Disclaimer
**This software is for EDUCATIONAL PURPOSES ONLY.** It is designed to simulate ransomware behavior for learning and research. Do not use this software for any illegal or malicious activities. The authors are not responsible for any misuse of this software.

## Project Structure

*   `server.py`: A Flask web server that hosts the informational UI and provides an endpoint to launch the simulation.
*   `rans.py`: A Python script using Tkinter that simulates a "Locked System" screen with a countdown timer and a decryption key requirement.
*   `index.html` / `templates/index.html`: The web interface for the educational case study.
*   `Test_files/`: A directory containing sample files for the simulation.
*   `static/`: Contains images and and other assets for the website.

## Features

- **Educational UI**: A web-based case study on high-profile information security incidents (Epstein Island).
- **Simulation Control**: An "ACCESS EPSTEIN FILES" button that handles safe simulation distribution.
- **Portable Simulation**: A standalone `.exe` (bundled in `.zip`) that provides a full-system lock without browser security warnings.
- **Real-Time Countdown**: A timer simulating an urgent system lock state.
- **Unlock Mechanism**: A key-based decryption simulation to restore access.

## Prerequisites

- Python 3.x
- Flask (`pip install flask`)
- Tkinter (usually comes pre-installed with Python on Windows)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/mahi-404/Ransomware-Simulation
cd Ransomware-Project
```

### 2. Run the Server
Start the Flask backend:
```bash
python server.py
```

### 3. Access the Interface
Open your browser and navigate to `http://127.0.0.1:5000`.

### 4. Run the Simulation
Click the **"ACCESS EPSTEIN FILES"** button in the "THE ISLAND FULL OF CRIMES" section. This will download the `Epstein_Files.zip`. Extract it and run the EXE inside to experience the full-system lock simulation.

## Note on Remote Access
Because this project uses a local Python backend and launches a Tkinter desktop window, it cannot be hosted directly on static hosting platforms like GitHub Pages. To share it online while keeping the local launch functionality, tools like **Ngrok** can be used to tunnel your local port `5000` to a public URL.

**To unlock the simulation:** Use the default key `UNLOCK123`.
