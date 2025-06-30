import tkinter as tk
from tkinter import messagebox
from datetime import datetime

#  Data Classes

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
    def __init__(self, enrollment_id, child, guardian, start_date, status):
        self.enrollment_id = enrollment_id
        self.child = child
        self.guardian = guardian
        self.start_date = start_date
        self.status = status

class Payment:
    def __init__(self, guardian_id, amount, receipt, payment_date):
        self.guardian_id = guardian_id
        self.amount = amount
        self.receipt = receipt
        self.payment_date = payment_date

class Attendance:
    def __init__(self, attendance_id, child_id, date):
        self.attendance_id = attendance_id
        self.child_id = child_id
        self.date = date


# GUI

class DaycareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daycare Center System")
        self.root.configure(bg="#c8a2c8")  # Light purple

        self.children = []
        self.guardians = []
        self.enrollments = []
        self.payments = []
        self.attendance_records = []

        #  Enrollment Fields
        tk.Label(root, text="Child Name", bg="#c8a2c8").grid(row=0, column=0)
        self.child_name = tk.Entry(root)
        self.child_name.grid(row=0, column=1)

        tk.Label(root, text="Age", bg="#c8a2c8").grid(row=1, column=0)
        self.child_age = tk.Entry(root)
        self.child_age.grid(row=1, column=1)

        tk.Label(root, text="Guardian Name", bg="#c8a2c8").grid(row=2, column=0)
        self.guardian_name = tk.Entry(root)
        self.guardian_name.grid(row=2, column=1)

        tk.Label(root, text="Contact Info", bg="#c8a2c8").grid(row=3, column=0)
        self.guardian_contact = tk.Entry(root)
        self.guardian_contact.grid(row=3, column=1)

        tk.Label(root, text="Address", bg="#c8a2c8").grid(row=4, column=0)
        self.guardian_address = tk.Entry(root)
        self.guardian_address.grid(row=4, column=1)

        #  Buttons

        btn_color = "#a678b7"  # medium purple

        tk.Button(root, text="Enroll Child", bg=btn_color, command=self.enroll_child).grid(row=5, columnspan=2, pady=6)
        tk.Button(root, text="Show Enrollments", bg=btn_color, command=self.show_enrollments).grid(row=6, columnspan=2, pady=2)
        tk.Button(root, text="Record Payment", bg=btn_color, command=self.record_payment).grid(row=7, columnspan=2, pady=2)
        tk.Button(root, text="Mark Attendance", bg=btn_color, command=self.mark_attendance).grid(row=8, columnspan=2, pady=2)
        tk.Button(root, text="View Total Attendance", bg=btn_color, command=self.show_attendance).grid(row=9, columnspan=2, pady=2)
        tk.Button(root, text="Show Attendance Per Student", bg=btn_color, command=self.show_individual_attendance).grid(row=10, columnspan=2, pady=4)

    def enroll_child(self):
        name = self.child_name.get()
        age = self.child_age.get()
        g_name = self.guardian_name.get()
        g_contact = self.guardian_contact.get()
        g_address = self.guardian_address.get()

        if name and age and g_name and g_contact and g_address:
            child = Child(len(self.children)+1, name, age)
            guardian = Guardian(len(self.guardians)+1, g_name, g_contact, g_address)
            enrollment = Enrollment(len(self.enrollments)+1, child, guardian, datetime.today().strftime("%Y-%m-%d"), "Active")

            self.children.append(child)
            self.guardians.append(guardian)
            self.enrollments.append(enrollment)

            messagebox.showinfo("Success", f"{name} enrolled successfully!")
            self.clear_fields()
        else:
            messagebox.showwarning("Incomplete", "Please fill all fields")

    def record_payment(self):
        if not self.guardians:
            messagebox.showinfo("Info", "No guardian enrolled")
            return

        guardian = self.guardians[-1]
        amount = "15000"
        receipt = f"RCT{len(self.payments)+1:03d}"
        payment_date = datetime.today().strftime("%Y-%m-%d")

        self.payments.append(Payment(guardian.guardian_id, amount, receipt, payment_date))
        messagebox.showinfo("Payment", f"Payment recorded: {receipt} - KES {amount}")

    def mark_attendance(self):
        if not self.children:
            messagebox.showinfo("Info", "No children enrolled")
            return

        today = datetime.today().strftime("%Y-%m-%d")
        for child in self.children:
            self.attendance_records.append(Attendance(len(self.attendance_records)+1, child.child_id, today))
        messagebox.showinfo("Attendance", "Today's attendance marked.")

    def show_enrollments(self):
        if self.enrollments:
            info = "\n".join([f"{e.child.name} - Guardian: {e.guardian.name} ({e.status})" for e in self.enrollments])
        else:
            info = "No enrollments yet."
        messagebox.showinfo("Enrollments", info)

    def show_attendance(self):
        if self.attendance_records:
            grouped = {}
            for record in self.attendance_records:
                grouped[record.date] = grouped.get(record.date, 0) + 1
            info = "\n".join([f"{day}: {count} present" for day, count in grouped.items()])
        else:
            info = "No attendance recorded yet."
        messagebox.showinfo("Total Attendance", info)

    def show_individual_attendance(self):
        if not self.attendance_records:
            messagebox.showinfo("Attendance", "No attendance recorded yet.")
            return

        attendance_count = {}
        for record in self.attendance_records:
            attendance_count[record.child_id] = attendance_count.get(record.child_id, 0) + 1

        details = []
        for child in self.children:
            count = attendance_count.get(child.child_id, 0)
            details.append(f"{child.name}: {count} days present")

        messagebox.showinfo("Student Attendance", "\n".join(details))

    def clear_fields(self):
        self.child_name.delete(0, tk.END)
        self.child_mark.delete(0, tk.END)
        self.guardian_name.delete(0, tk.END)
        self.guardian_contact.delete(0, tk.END)
        self.guardian_address.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = DaycareApp(root)
    root.mainloop()
