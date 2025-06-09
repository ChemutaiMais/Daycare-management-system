import tkinter as tk
from tkinter import messagebox, simpledialog, Label, Entry, W

# Create main window
root = tk.Tk()
root.title("Sequence Structure")
root.configure(background="Pink")
root.geometry("800x800")
 
# Label for input
L1 = Label(root, text="Series")
L1.grid(row=0, sticky=W)

# Entry field
E1 = Entry(root, width=40)

root.mainloop()



