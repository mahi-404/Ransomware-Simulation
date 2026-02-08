import tkinter as tk
import time
import threading

# ================= CONFIG =================
UNLOCK_KEY = "UNLOCK123"
LOCK_TIME = 900 # seconds (5 minutes)
# ==========================================

class LockerwareSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Lockerware Simulator")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        # Disable close actions
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.root.bind("<Alt-F4>", self.disable_event)
        self.root.bind("<Escape>", self.disable_event)

        self.time_left = LOCK_TIME

        self.create_ui()
        self.start_timer()

    def disable_event(self, event=None):
        pass  # Intentionally block closing

    def create_ui(self):
        title = tk.Label(
            self.root,
            text=("YOUR SYSTEM HAS BEEN LOCKED😝\n\n"
                "TO UNLOCK TRANSFER AMOUNT INR 999999/- ONLY\n\n"
            ),
            fg="red",
            bg="black",
            font=("Arial", 40, "bold")
        )
        title.pack(pady=30)

        msg = tk.Label(
            self.root,
            text=(
                "All your system access has been restricted.\n\n"
                "To regain access, enter the decryption key.\n\n"
                "Failure to do so will result in permanent lock."
            ),
            fg="white",
            bg="black",
            font=("Arial", 18),
            justify="center"
        )
        msg.pack(pady=20)

        self.timer_label = tk.Label(
            self.root,
            text="Time Left: --:--",
            fg="yellow",
            bg="black",
            font=("Arial", 22)
        )
        self.timer_label.pack(pady=20)

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
            text="UNLOCK",
            font=("Arial", 14),
            bg="red",
            fg="white",
            command=self.check_key
        )
        unlock_btn.pack(pady=20)

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
        if entered_key == UNLOCK_KEY:
            self.unlock_system()
        else:
            self.status_label.config(text="Invalid key. Try again.")

    def unlock_system(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LockerwareSimulator(root)
    root.mainloop()