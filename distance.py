import tkinter as tk
from tkinter import messagebox

def calculate_speed():
    try:
        distance = float(distance_entry.get())
        time = float(time_entry.get())
        if time > 0:
            speed = distance / time
            messagebox.showinfo("Speed Calculation", f"Speed of the journey: {speed:.2f} km/h")
        else:
            messagebox.showerror("Input Error", "Time must be greater than zero.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for distance and time.")


root = tk.Tk()
root.title("Speed Calculator")
tk.Label(root, text="Enter Distance (km):").grid(row=0, column=0)
distance_entry = tk.Entry(root)
distance_entry.grid(row=0, column=1)


tk.Label(root, text="Enter Time (hours):").grid(row=1, column=0)
time_entry = tk.Entry(root)
time_entry.grid(row=1, column=1)


calculate_button = tk.Button(root, text="Calculate Speed", command=calculate_speed)
calculate_button.grid(row=2, columnspan=2)


root.mainloop()
