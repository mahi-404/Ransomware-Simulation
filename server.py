from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import base64
import sys
import subprocess

app = Flask(__name__)

# Config
UNLOCK_KEY = "UNLOCK123"
TARGET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Test_files")

@app.route('/')
def home():
    return render_template('index.html')

def encrypt_test_files():
    if not os.path.exists(TARGET_DIR): return
    for filename in os.listdir(TARGET_DIR):
        file_path = os.path.join(TARGET_DIR, filename)
        if os.path.isdir(file_path) or filename.endswith(".locked") or filename == "README_RESTORE.txt":
            continue
        try:
            with open(file_path, "rb") as f: content = f.read()
            encoded = base64.b64encode(content)
            with open(file_path, "wb") as f: f.write(encoded)
            os.rename(file_path, file_path + ".locked")
        except Exception as e: print(f"Error locking {filename}: {e}")

def decrypt_test_files():
    if not os.path.exists(TARGET_DIR): return
    for filename in os.listdir(TARGET_DIR):
        if not filename.endswith(".locked"): continue
        locked_path = os.path.join(TARGET_DIR, filename)
        original_path = locked_path[:-7]
        try:
            with open(locked_path, "rb") as f: encoded = f.read()
            decoded = base64.b64decode(encoded)
            with open(locked_path, "wb") as f: f.write(decoded)
            os.rename(locked_path, original_path)
        except Exception as e: print(f"Error unlocking {filename}: {e}")

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    try:
        encrypt_test_files()
        
        # Launch the desktop simulation script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, 'rans.py')
        subprocess.Popen([sys.executable, script_path], cwd=current_dir)
        
        return jsonify({'status': 'success', 'message': 'Full-system simulation started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/verify-key', methods=['POST'])
def verify_key():
    data = request.get_json()
    if data.get('key') == UNLOCK_KEY:
        decrypt_test_files()
        return jsonify({'status': 'success', 'message': 'Key verified, files restored'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid key'}), 401

@app.route('/download-simulation')
def download_simulation():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
    return send_from_directory(directory, 'Epstein_Files.zip', as_attachment=True)

if __name__ == '__main__':
    # Use host='0.0.0.0' to be accessible on VPS
    app.run(debug=True, host='0.0.0.0')
