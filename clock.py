import tkinter as tk
from tkinter import messagebox
import time

class CountdownClock:
    def __init__(self, master):
        self.master = master
        self.master.title("Countdown Clock")
        self.master.geometry("300x150")

        self.time_left = 0
        self.running = False

        self.label = tk.Label(master, text="Enter time in seconds:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, font=("Arial", 12))
        self.entry.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_countdown)
        self.start_button.pack(pady=10)

        self.time_display = tk.Label(master, text="", font=("Arial", 20))
        self.time_display.pack()

    def start_countdown(self):
        try:
            self.time_left = int(self.entry.get())
            if self.time_left <= 0:
                raise ValueError
            self.running = True
            self.countdown()
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive integer!")

    def countdown(self):
        if self.running:
            if self.time_left <= 0:
                self.time_display.config(text="Time's up!")
                self.running = False
            else:
                mins, secs = divmod(self.time_left, 60)
                timeformat = f"{mins:02d}:{secs:02d}"
                self.time_display.config(text=timeformat)
                self.time_left -= 1
                self.master.after(1000, self.countdown)

def main():
    root = tk.Tk()
    CountdownClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()