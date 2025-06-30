import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import re

# Data Classes
class Child:
    def __init__(self, child_id, name, age):
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
    def __init__(self, payment_id, child_id, amount, receipt, payment_date, month):
        self.payment_id = payment_id
        self.child_id = child_id
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
        self.root.configure(bg="#F5F6F5") 

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

    # New validation for phone numbers
    def validate_phone(self, phone):
        # Basic validation: numeric, and between 7 to 15 digits 
        return phone.isdigit() and 7 <= len(phone) <= 15

    def setup_enrollment_tab(self):
        form_frame = tk.Frame(self.enrollment_tab, bg="#F5F6F5")
        form_frame.pack(pady=10, padx=10, fill="x")

        # Child Fields
        ttk.Label(form_frame, text="Child Name").grid(row=0, column=0, sticky="w", pady=5)
        self.child_name = ttk.Entry(form_frame)
        self.child_name.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Age").grid(row=1, column=0, sticky="w", pady=5)
        self.child_age = ttk.Entry(form_frame)
        self.child_age.grid(row=1, column=1, sticky="ew", pady=5)

        # Guardian Fields
        ttk.Label(form_frame, text="Guardian Name").grid(row=2, column=0, sticky="w", pady=5)
        self.guardian_name = ttk.Entry(form_frame)
        self.guardian_name.grid(row=2, column=1, sticky="ew", pady=5)

        # Changed label from 'Guardian Contact (Email)' to 'Guardian Contact (Phone No.)'
        ttk.Label(form_frame, text="Guardian Contact (Phone No.)").grid(row=3, column=0, sticky="w", pady=5)
        self.guardian_contact = ttk.Entry(form_frame)
        self.guardian_contact.grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Guardian Address").grid(row=4, column=0, sticky="w", pady=5)
        self.guardian_address = ttk.Entry(form_frame)
        self.guardian_address.grid(row=4, column=1, sticky="ew", pady=5)

        # Buttons
        btn_frame = tk.Frame(self.enrollment_tab, bg="#F5F6F5")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Enroll Child", command=self.enroll_child).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_enrollment_fields).pack(side="left", padx=5)

    def setup_payment_tab(self):
        form_frame = tk.Frame(self.payment_tab, bg="#F5F6F5")
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Child ID").grid(row=0, column=0, sticky="w", pady=5)
        self.payment_child_id = ttk.Entry(form_frame)
        self.payment_child_id.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Amount").grid(row=1, column=0, sticky="w", pady=5)
        self.payment_amount = ttk.Entry(form_frame)
        self.payment_amount.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Month (e.g., January)").grid(row=2, column=0, sticky="w", pady=5)
        self.payment_month = ttk.Entry(form_frame)
        self.payment_month.grid(row=2, column=1, sticky="ew", pady=5)

        btn_frame = tk.Frame(self.payment_tab, bg="#F5F6F5")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Record Payment", command=self.record_payment).pack(side="left", padx=5)

    def setup_attendance_tab(self):
        form_frame = tk.Frame(self.attendance_tab, bg="#F5F6F5")
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Child IDs (comma-separated)").grid(row=0, column=0, sticky="w", pady=5)
        self.attendance_ids = ttk.Entry(form_frame)
        self.attendance_ids.grid(row=0, column=1, sticky="ew", pady=5)

        btn_frame = tk.Frame(self.attendance_tab, bg="#F5F6F5")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Mark Attendance", command=self.mark_attendance).pack(side="left", padx=5)

    def setup_staff_tab(self):
        form_frame = tk.Frame(self.staff_tab, bg="#F5F6F5")
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Staff Name").grid(row=0, column=0, sticky="w", pady=5)
        self.staff_name = ttk.Entry(form_frame)
        self.staff_name.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Role").grid(row=1, column=0, sticky="w", pady=5)
        self.staff_role = ttk.Entry(form_frame)
        self.staff_role.grid(row=1, column=1, sticky="ew", pady=5)

        # Changed label from 'Contact' to 'Contact (Phone No.)'
        ttk.Label(form_frame, text="Contact (Phone No.)").grid(row=2, column=0, sticky="w", pady=5)
        self.staff_contact = ttk.Entry(form_frame)
        self.staff_contact.grid(row=2, column=1, sticky="ew", pady=5)

        btn_frame = tk.Frame(self.staff_tab, bg="#F5F6F5")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Register Staff", command=self.register_staff).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_staff_fields).pack(side="left", padx=5)

    def setup_reports_tab(self):
        btn_frame = tk.Frame(self.reports_tab, bg="#F5F6F5")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="View Enrollments", command=self.show_enrollments).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="View Payments", command=self.show_payments).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="View Attendance", command=self.show_attendance).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="View Staff", command=self.show_staff).pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="View Individual Attendance", command=self.show_individual_attendance).pack(pady=5, fill="x")

        # Treeview for displaying reports
        self.report_tree = ttk.Treeview(self.reports_tab, columns=(), show="headings")
        self.report_tree.pack(pady=10, fill="both", expand=True)

    def enroll_child(self):
        name = self.child_name.get().strip()
        age = self.child_age.get().strip()
        g_name = self.guardian_name.get().strip()
        g_contact = self.guardian_contact.get().strip() # This is now phone number
        g_address = self.guardian_address.get().strip()

        if not all([name, age, g_name, g_contact, g_address]):
            messagebox.showwarning("Incomplete", "Please fill all fields")
            return
        if not age.isdigit() or int(age) < 0 or int(age) > 12:
            messagebox.showwarning("Invalid Input", "Age must be a number between 0 and 12")
            return
        # Changed  to phone number
        if not self.validate_phone(g_contact):
            messagebox.showwarning("Invalid Input", "Please enter a valid phone number for guardian contact (7-15 digits, numeric only).")
            return

        child_id = self.generate_id('C', self.children)
        guardian_id = self.generate_id('G', self.guardians)
        enrollment_id = self.generate_id('E', self.enrollments)

        child = {
            'id': child_id,
            'name': name,
            'age': int(age)
        }
        guardian = {
            'id': guardian_id,
            'name': g_name,
            'contact_info': g_contact, # Storing phone number
            'address': g_address
        }
        enrollment = {
            'id': enrollment_id,
            'child_id': child_id,
            'guardian_id': guardian_id,
            'start_date': datetime.today().strftime("%Y-%m-%d"),
            'status': 'Active'
        }

        self.children.append(child)
        self.guardians.append(guardian)
        self.enrollments.append(enrollment)
        self.save_data()
        messagebox.showinfo("Success", f"{name} enrolled successfully with ID: {child_id}")
        self.clear_enrollment_fields()

    def record_payment(self):
        child_id = self.payment_child_id.get().strip()
        amount = self.payment_amount.get().strip()
        month = self.payment_month.get().strip()

        if not all([child_id, amount, month]):
            messagebox.showwarning("Incomplete", "Please fill all fields")
            return
        if not any(c['id'] == child_id for c in self.children):
            messagebox.showwarning("Invalid Input", "Child ID not found")
            return
        try:
            float_amount = float(amount)
            if float_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Input", "Amount must be a positive number")
            return

        payment_id = self.generate_id('P', self.payments)
        receipt = f"RCT{payment_id}"
        payment = {
            'id': payment_id,
            'child_id': child_id,
            'amount': float_amount,
            'receipt': receipt,
            'payment_date': datetime.today().strftime("%Y-%m-%d"),
            'month': month,
            'status': 'Paid'
        }
        self.payments.append(payment)
        self.save_data()
        messagebox.showinfo("Success", f"Payment recorded: {receipt} - KES {amount} for {month}")

    def mark_attendance(self):
        ids = self.attendance_ids.get().strip()
        if not ids:
            messagebox.showwarning("Incomplete", "Please enter child IDs")
            return

        date = datetime.today().strftime("%Y-%m-%d")
        present_ids = [cid.strip() for cid in ids.split(',') if any(c['id'] == cid.strip() for c in self.children)]
        if not present_ids:
            messagebox.showwarning("Invalid Input", "No valid child IDs found")
            return

        for cid in present_ids:
            attendance_id = self.generate_id('A', self.attendance)
            self.attendance.append({
                'id': attendance_id,
                'child_id': cid,
                'date': date
            })
        self.save_data()
        messagebox.showinfo("Success", f"Attendance recorded for {date}")

    def register_staff(self):
        name = self.staff_name.get().strip()
        role = self.staff_role.get().strip()
        contact = self.staff_contact.get().strip() # This is now phone number

        if not all([name, role, contact]):
            messagebox.showwarning("Incomplete", "Please fill all fields")
            return
        # Change to phone
        if not self.validate_phone(contact):
            messagebox.showwarning("Invalid Input", "Please enter a valid phone number for staff contact (7-15 digits, numeric only).")
            return

        staff_id = self.generate_id('S', self.staff)
        staff = {
            'id': staff_id,
            'name': name,
            'role': role,
            'contact': contact
        }
        self.staff.append(staff)
        self.save_data()
        messagebox.showinfo("Success", f"Staff registered with ID: {staff_id}")
        self.clear_staff_fields()

    def show_enrollments(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        self.report_tree["columns"] = ("Child ID", "Child Name", "Age", "Guardian", "Guardian Phone", "Status", "Start Date")
        for col in self.report_tree["columns"]:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=100)

        for e in self.enrollments:
            child = next((c for c in self.children if c['id'] == e['child_id']), None)
            guardian = next((g for g in self.guardians if g['id'] == e['guardian_id']), None)
            if child and guardian:
                self.report_tree.insert("", "end", values=(e['child_id'], child['name'], child['age'], guardian['name'], guardian['contact_info'], e['status'], e['start_date']))

    def show_payments(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        self.report_tree["columns"] = ("Receipt", "Child Name", "Amount", "Month", "Date", "Status")
        for col in self.report_tree["columns"]:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=100)

        for p in self.payments:
            child = next((c for c in self.children if c['id'] == p['child_id']), None)
            child_name = child['name'] if child else "Unknown"
            self.report_tree.insert("", "end", values=(p['receipt'], child_name, p['amount'], p['month'], p['payment_date'], p['status']))

    def show_attendance(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        self.report_tree["columns"] = ("Date", "Child IDs")
        for col in self.report_tree["columns"]:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=150)

        grouped = {}
        for record in self.attendance:
            grouped[record['date']] = grouped.get(record['date'], []) + [record['child_id']]
        for date, ids in grouped.items():
            self.report_tree.insert("", "end", values=(date, ", ".join(ids)))

    def show_staff(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        self.report_tree["columns"] = ("Staff ID", "Name", "Role", "Phone No.")
        for col in self.report_tree["columns"]:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=100)

        for s in self.staff:
            self.report_tree.insert("", "end", values=(s['id'], s['name'], s['role'], s['contact']))

    def show_individual_attendance(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        self.report_tree["columns"] = ("Child ID", "Child Name", "Days Present")
        for col in self.report_tree["columns"]:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=100)

        attendance_count = {}
        for record in self.attendance:
            attendance_count[record['child_id']] = attendance_count.get(record['child_id'], 0) + 1
        for child in self.children:
            count = attendance_count.get(child['id'], 0)
            self.report_tree.insert("", "end", values=(child['id'], child['name'], count))

    def clear_enrollment_fields(self):
        self.child_name.delete(0, tk.END)
        self.child_age.delete(0, tk.END)
        self.guardian_name.delete(0, tk.END)
        self.guardian_contact.delete(0, tk.END)
        self.guardian_address.delete(0, tk.END)

    def clear_staff_fields(self):
        self.staff_name.delete(0, tk.END)
        self.staff_role.delete(0, tk.END)
        self.staff_contact.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DaycareApp(root)
    root.mainloop()