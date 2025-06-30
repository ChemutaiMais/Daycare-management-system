import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json
import os
import re

# Data Classes
class Child:
    def __init__(self, child_id, name, age): # Removed average_mark
        self.child_id = child_id
        self.name = name
        self.age = age

class Guardian:
    def __init__(self, guardian_id, name, contact_info, address):
        self.guardian_id = guardian_id
        self.name = name
        self.contact_info = contact_info
        self.address = address

class Enrollment:
    def __init__(self, enrollment_id, child_id, guardian_id, start_date, status):
        self.enrollment_id = enrollment_id
        self.child_id = child_id
        self.guardian_id = guardian_id
        self.start_date = start_date
        self.status = status

class Payment:
    def __init__(self, payment_id, guardian_id, amount, receipt, payment_date, month):
        self.payment_id = payment_id
        self.guardian_id = guardian_id
        self.amount = amount
        self.receipt = receipt
        self.payment_date = payment_date
        self.month = month

class Attendance:
    def __init__(self, attendance_id, child_id, date):
        self.attendance_id = attendance_id
        self.child_id = child_id
        self.date = date

class Staff:
    def __init__(self, staff_id, name, role, contact):
        self.staff_id = staff_id
        self.name = name
        self.role = role
        self.contact = contact

# Daycare Management System
class DaycareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taskmaster Daycare System")
        self.root.geometry("800x600")
        self.root.configure(bg="#F5F6F5")  # Light gray background

        # Data storage
        self.data_files = {
            'children': 'children.json',
            'guardians': 'guardians.json',
            'enrollments': 'enrollments.json',
            'payments': 'payments.json',
            'attendance': 'attendance.json',
            'staff': 'staff.json'
        }
        self.load_data()

        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=10)
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#F5F6F5")
        self.style.configure("TEntry", font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("Treeview", font=("Segoe UI", 10))

        # Header
        header_frame = tk.Frame(self.root, bg="#0052CC")  # Corporate blue
        header_frame.pack(fill="x", pady=10)
        tk.Label(header_frame, text="Taskmaster Daycare Management System", font=("Segoe UI", 16, "bold"), fg="white", bg="#0052CC").pack(pady=10)

        # Tabbed Interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, fill="both", expand=True)

        # Tabs
        self.enrollment_tab = tk.Frame(self.notebook, bg="#F5F6F5")
        self.payment_tab = tk.Frame(self.notebook, bg="#F5F6F5")
        self.attendance_tab = tk.Frame(self.notebook, bg="#F5F6F5")
        self.staff_tab = tk.Frame(self.notebook, bg="#F5F6F5")
        self.reports_tab = tk.Frame(self.notebook, bg="#F5F6F5")

        self.notebook.add(self.enrollment_tab, text="Enrollment")
        self.notebook.add(self.payment_tab, text="Payments")
        self.notebook.add(self.attendance_tab, text="Attendance")
        self.notebook.add(self.staff_tab, text="Staff")
        self.notebook.add(self.reports_tab, text="Reports")

        self.setup_enrollment_tab()
        self.setup_payment_tab()
        self.setup_attendance_tab()
        self.setup_staff_tab()
        self.setup_reports_tab()

    def load_data(self):
        for key, file in self.data_files.items():
            if os.path.exists(file):
                with open(file, 'r') as f:
                    setattr(self, key, json.load(f))
            else:
                setattr(self, key, [])

    def save_data(self):
        for key, file in self.data_files.items():
            with open(file, 'w') as f:
                json.dump(getattr(self, key), f, indent=2)

    def generate_id(self, prefix, collection):
        return f"{prefix}{len(collection) + 1:03d}"

    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def setup_enrollment_tab(self):
        form_frame = tk.Frame(self.enrollment_tab, bg="#F5F6F5")
        form_frame.pack(pady=10, padx=10, fill="x")

        # Child Fields
        ttk.Label(form_frame, text="Child Name").grid(row=0, column=0, sticky="w", pady=5)
        self.child_name = ttk.Entry(form_frame)
        self.child_name.grid