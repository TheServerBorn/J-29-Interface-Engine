import json
import tkinter as tk
from pathlib import Path

DEBUG_FILE = Path("config/aux_display_debug.json")
POLL_MS = 100


class AuxDisplaySimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("J-29 Aux Display Simulator")
        self.root.geometry("420x180")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.state_label = tk.Label(
            self.root,
            text="WAITING",
            font=("Courier New", 11, "bold"),
        )
        self.state_label.pack(pady=(18, 4))

        self.line1_label = tk.Label(
            self.root,
            text="J-29",
            font=("Courier New", 18, "bold"),
        )
        self.line1_label.pack(pady=2)

        self.line2_label = tk.Label(
            self.root,
            text="NO DATA",
            font=("Courier New", 16),
        )
        self.line2_label.pack(pady=2)

        self.last_mtime = None
        self.poll()

    def read_state(self):
        if not DEBUG_FILE.exists():
            return {
                "state": "WAITING",
                "line1": "J-29",
                "line2": "NO DEBUG DATA",
            }

        try:
            with DEBUG_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return None

    def poll(self):
        try:
            mtime = DEBUG_FILE.stat().st_mtime if DEBUG_FILE.exists() else None
        except OSError:
            mtime = None

        if mtime != self.last_mtime:
            self.last_mtime = mtime
            data = self.read_state()

            if data:
                state = str(data.get("state", "STATUS"))
                line1 = str(data.get("line1", ""))
                line2 = str(data.get("line2", ""))

                self.state_label.config(text=state)
                self.line1_label.config(text=line1)
                self.line2_label.config(text=line2)

        self.root.after(POLL_MS, self.poll)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    AuxDisplaySimulator().run()
