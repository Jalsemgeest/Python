

print("RUNNING Test")

import tkinter as tk
from tkinter import ttk

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Timer")
        self.initialize_ui()
        self.time_left = 0
        self.timer_running = False

    def initialize_ui(self):
        self.time_display = ttk.Label(self.root, text="00:00", font=("Helvetica", 48))
        self.time_display.pack(pady=20)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=(20, 10))

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = ttk.Button(self.root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=(10, 20))

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.time_left = 0
        self.update_display("00:00")
        self.stop_timer()

    def update_timer(self):
        if self.timer_running:
            self.time_left += 1
            mins, secs = divmod(self.time_left, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            self.update_display(time_format)
            self.root.after(1000, self.update_timer)

    def update_display(self, time_to_show):
        self.time_display.config(text=time_to_show)

def main():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
