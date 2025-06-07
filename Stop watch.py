import tkinter as tk
from tkinter import messagebox
import time
import math

class StopwatchCountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch & Countdown Timer with Clock")
        self.root.geometry("900x600")
        self.root.configure(bg="#222222")

        # --------- Top: Centered Digital + Analog Clock ---------
        top_frame = tk.Frame(root, bg="#222222")
        top_frame.pack(side=tk.TOP, pady=20)

        self.digital_clock_label = tk.Label(top_frame, font=("Arial", 32, "bold"),
                                            fg="cyan", bg="#222222")
        self.digital_clock_label.pack()
        self.update_digital_clock()

        self.analog_canvas = tk.Canvas(top_frame, width=200, height=200, bg="#222222", highlightthickness=0)
        self.analog_canvas.pack(pady=10)
        self.center_x, self.center_y, self.clock_radius = 100, 100, 90
        self.draw_clock_face()
        self.update_analog_clock()

        # --------- Middle: Stopwatch and Countdown ---------
        main_frame = tk.Frame(root, bg="#222222")
        main_frame.pack(expand=True, fill=tk.BOTH, pady=20)

        # Stopwatch
        stopwatch_frame = tk.Frame(main_frame, bg="#111111", bd=2, relief=tk.RIDGE)
        stopwatch_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        tk.Label(stopwatch_frame, text="Stopwatch", font=("Arial", 20, "bold"), fg="lime", bg="#111111").pack(pady=10)

        self.stopwatch_label = tk.Label(stopwatch_frame, text="00:00:00.000",
                                        font=("Arial", 28, "bold"), fg="lime", bg="#111111")
        self.stopwatch_label.pack(pady=10)

        btn_frame = tk.Frame(stopwatch_frame, bg="#111111")
        btn_frame.pack(pady=10)

        self.stopwatch_running = False
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed = 0.0
        self.laps = []

        self.start_stop_btn = tk.Button(btn_frame, text="Start", width=10, command=self.stopwatch_start_stop)
        self.start_stop_btn.grid(row=0, column=0, padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Reset", width=10, command=self.stopwatch_reset)
        self.reset_btn.grid(row=0, column=1, padx=5)

        self.lap_btn = tk.Button(btn_frame, text="Lap", width=10, command=self.record_lap, state="disabled")
        self.lap_btn.grid(row=0, column=2, padx=5)

        self.clear_laps_btn = tk.Button(btn_frame, text="Clear Laps", width=10, command=self.clear_laps)
        self.clear_laps_btn.grid(row=0, column=3, padx=5)

        self.laps_listbox = tk.Listbox(stopwatch_frame, width=40, height=10, font=("Arial", 12))
        self.laps_listbox.pack(pady=10)

        # Countdown
        countdown_frame = tk.Frame(main_frame, bg="#111111", bd=2, relief=tk.RIDGE)
        countdown_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        tk.Label(countdown_frame, text="Countdown Timer", font=("Arial", 20, "bold"), fg="orange", bg="#111111").pack(pady=10)

        input_frame = tk.Frame(countdown_frame, bg="#111111")
        input_frame.pack(pady=10)

        self.hour_var = tk.StringVar(value="00")
        self.min_var = tk.StringVar(value="00")
        self.sec_var = tk.StringVar(value="00")

        self.hour_entry = tk.Entry(input_frame, width=3, font=("Arial", 24), justify="center",
                                   textvariable=self.hour_var, bg="#333333", fg="white", insertbackground="white")
        self.hour_entry.grid(row=0, column=0)

        tk.Label(input_frame, text=":", font=("Arial", 24), fg="orange", bg="#111111").grid(row=0, column=1)

        self.min_entry = tk.Entry(input_frame, width=3, font=("Arial", 24), justify="center",
                                  textvariable=self.min_var, bg="#333333", fg="white", insertbackground="white")
        self.min_entry.grid(row=0, column=2)

        tk.Label(input_frame, text=":", font=("Arial", 24), fg="orange", bg="#111111").grid(row=0, column=3)

        self.sec_entry = tk.Entry(input_frame, width=3, font=("Arial", 24), justify="center",
                                  textvariable=self.sec_var, bg="#333333", fg="white", insertbackground="white")
        self.sec_entry.grid(row=0, column=4)

        self.countdown_start_btn = tk.Button(countdown_frame, text="Start Countdown",
                                             width=20, height=2, command=self.start_countdown)
        self.countdown_start_btn.pack(pady=10)

        self.countdown_label = tk.Label(countdown_frame, text="", font=("Arial", 28, "bold"),
                                        fg="orange", bg="#111111")
        self.countdown_label.pack(pady=10)

        self.countdown_running = False
        self.countdown_time_left = 0

    # ---------- Digital Clock ----------
    def update_digital_clock(self):
        now = time.strftime("%H:%M:%S")
        self.digital_clock_label.config(text=now)
        self.root.after(1000, self.update_digital_clock)

    # ---------- Analog Clock ----------
    def draw_clock_face(self):
        self.analog_canvas.delete("all")
        self.analog_canvas.create_oval(self.center_x - self.clock_radius, self.center_y - self.clock_radius,
                                       self.center_x + self.clock_radius, self.center_y + self.clock_radius,
                                       outline="cyan", width=4)
        for i in range(12):
            angle = math.pi / 6 * i
            x_start = self.center_x + (self.clock_radius - 20) * math.sin(angle)
            y_start = self.center_y - (self.clock_radius - 20) * math.cos(angle)
            x_end = self.center_x + self.clock_radius * math.sin(angle)
            y_end = self.center_y - self.clock_radius * math.cos(angle)
            self.analog_canvas.create_line(x_start, y_start, x_end, y_end, fill="cyan", width=3)

    def update_analog_clock(self):
        self.draw_clock_face()
        now = time.localtime()
        sec, min, hr = now.tm_sec, now.tm_min, now.tm_hour % 12

        sec_angle = math.pi * 2 * sec / 60
        min_angle = math.pi * 2 * (min + sec / 60) / 60
        hr_angle = math.pi * 2 * (hr + min / 60) / 12

        sec_x = self.center_x + (self.clock_radius - 30) * math.sin(sec_angle)
        sec_y = self.center_y - (self.clock_radius - 30) * math.cos(sec_angle)
        self.analog_canvas.create_line(self.center_x, self.center_y, sec_x, sec_y, fill="red", width=1)

        min_x = self.center_x + (self.clock_radius - 50) * math.sin(min_angle)
        min_y = self.center_y - (self.clock_radius - 50) * math.cos(min_angle)
        self.analog_canvas.create_line(self.center_x, self.center_y, min_x, min_y, fill="white", width=3)

        hr_x = self.center_x + (self.clock_radius - 80) * math.sin(hr_angle)
        hr_y = self.center_y - (self.clock_radius - 80) * math.cos(hr_angle)
        self.analog_canvas.create_line(self.center_x, self.center_y, hr_x, hr_y, fill="white", width=5)

        self.root.after(1000, self.update_analog_clock)

    # ---------- Stopwatch ----------
    def stopwatch_start_stop(self):
        if not self.stopwatch_running:
            self.stopwatch_start_time = time.perf_counter() - self.stopwatch_elapsed
            self.stopwatch_running = True
            self.start_stop_btn.config(text="Stop")
            self.lap_btn.config(state="normal")
            self.update_stopwatch()
        else:
            self.stopwatch_elapsed = time.perf_counter() - self.stopwatch_start_time
            self.stopwatch_running = False
            self.start_stop_btn.config(text="Start")
            self.lap_btn.config(state="disabled")

    def update_stopwatch(self):
        if self.stopwatch_running:
            elapsed = time.perf_counter() - self.stopwatch_start_time
            self.display_stopwatch_time(elapsed)
            self.root.after(10, self.update_stopwatch)

    def display_stopwatch_time(self, elapsed):
        hrs = int(elapsed // 3600)
        mins = int((elapsed % 3600) // 60)
        secs = int(elapsed % 60)
        millis = int((elapsed - int(elapsed)) * 1000)
        self.stopwatch_label.config(text=f"{hrs:02}:{mins:02}:{secs:02}.{millis:03}")

    def stopwatch_reset(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0.0
        self.start_stop_btn.config(text="Start")
        self.lap_btn.config(state="disabled")
        self.display_stopwatch_time(0)
        self.clear_laps()

    def record_lap(self):
        if self.stopwatch_running:
            elapsed = time.perf_counter() - self.stopwatch_start_time
            lap_time = self.format_time(elapsed)
            self.laps.append(lap_time)
            self.laps_listbox.insert(tk.END, f"Lap {len(self.laps)}: {lap_time}")

    def clear_laps(self):
        self.laps.clear()
        self.laps_listbox.delete(0, tk.END)

    def format_time(self, elapsed):
        hrs = int(elapsed // 3600)
        mins = int((elapsed % 3600) // 60)
        secs = int(elapsed % 60)
        millis = int((elapsed - int(elapsed)) * 1000)
        return f"{hrs:02}:{mins:02}:{secs:02}.{millis:03}"

    # ---------- Countdown ----------
    def start_countdown(self):
        if self.countdown_running:
            self.countdown_running = False
            self.countdown_start_btn.config(text="Start Countdown")
            self.countdown_label.config(text="")
        else:
            try:
                h = int(self.hour_var.get())
                m = int(self.min_var.get())
                s = int(self.sec_var.get())
                total_seconds = h * 3600 + m * 60 + s
                if total_seconds <= 0:
                    messagebox.showerror("Error", "Set a time greater than zero.")
                    return
                self.countdown_time_left = total_seconds
                self.countdown_running = True
                self.countdown_start_btn.config(text="Stop Countdown")
                self.update_countdown()
            except:
                messagebox.showerror("Error", "Invalid input.")

    def update_countdown(self):
        if self.countdown_running and self.countdown_time_left >= 0:
            hrs = self.countdown_time_left // 3600
            mins = (self.countdown_time_left % 3600) // 60
            secs = self.countdown_time_left % 60
            self.countdown_label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")
            if self.countdown_time_left == 0:
                self.countdown_running = False
                self.countdown_start_btn.config(text="Start Countdown")
                messagebox.showinfo("Countdown Finished", "Time's up!")
            else:
                self.countdown_time_left -= 1
                self.root.after(1000, self.update_countdown)

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchCountdownApp(root)
    root.mainloop()
