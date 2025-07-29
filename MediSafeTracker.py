import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime, timedelta
from plyer import notification
import os

FILENAME = "medicine_data.csv"

# Save medicine
def save_data():
    name = name_entry.get()
    dosage = dosage_entry.get()
    quantity = quantity_entry.get()
    expiry = expiry_entry.get()
    description = description_entry.get()

    if not name or not dosage or not quantity or not expiry or not description:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
        quantity = int(quantity)
    except:
        messagebox.showerror("Format Error", "Date must be YYYY-MM-DD and quantity must be a number.")
        return

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, dosage, quantity, expiry, description])

    messagebox.showinfo("Saved", f"{name} added successfully!")
    clear_inputs()
    load_data()
    check_alerts()
#delete data
def delete_selected():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a medicine to delete.")
        return

    item_id = selected[0]
    values = list(table.item(item_id, "values"))  

    updated_rows = []
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row != values:
                    updated_rows.append(row)

        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        messagebox.showinfo("Deleted", f"{values[0]} has been deleted.")
        load_data()

    except FileNotFoundError:
        messagebox.showerror("File Error", "Medicine data file not found.")


# Alerts
def check_alerts():
    today = datetime.today().date()
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 5:
                    continue
                name, dose, qty, expiry, desc = row
                try:
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                    qty = int(qty)
                except:
                    continue

                # Expiry alert
                days_left = (expiry_date - today).days
                if 0 <= days_left <= 3:
                    show_notification(f"Expiry Alert: {name} expires on {expiry_date}")

                # Low quantity alert
                if qty <= 3:
                    show_notification(f"Low Stock: Only {qty} left of {name}")

    except FileNotFoundError:
        pass

def show_notification(message):
    notification.notify(
        title="Medicine Reminder",
        message=message,
        timeout=5
    )

# Load data
def load_data():
    for row in table.get_children():
        table.delete(row)
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                table.insert('', tk.END, values=row)
    except FileNotFoundError:
        pass

def view_summary():
    messagebox.showinfo("Summary", "This feature will show medicine summary (to be implemented).")

def view_medicine():
    load_data()
    messagebox.showinfo("View Medicine", "Medicines loaded in table below.")

def clear_inputs():
    name_entry.delete(0, tk.END)
    dosage_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    expiry_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Medicine Reminder App")
root.geometry("720x570")
root.resizable(False, False)

# Input Frame
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Medicine Name").grid(row=0, column=0, padx=5, pady=3)
name_entry = tk.Entry(form_frame, width=40)
name_entry.grid(row=0, column=1)

tk.Label(form_frame, text="Dosage (e.g., 1 pill/day)").grid(row=1, column=0, padx=5, pady=3)
dosage_entry = tk.Entry(form_frame, width=40)
dosage_entry.grid(row=1, column=1)

tk.Label(form_frame, text="Quantity").grid(row=2, column=0, padx=5, pady=3)
quantity_entry = tk.Entry(form_frame, width=40)
quantity_entry.grid(row=2, column=1)

tk.Label(form_frame, text="Expiry Date (YYYY-MM-DD)").grid(row=3, column=0, padx=5, pady=3)
expiry_entry = tk.Entry(form_frame, width=40)
expiry_entry.grid(row=3, column=1)

tk.Label(form_frame, text="Description").grid(row=4, column=0, padx=5, pady=3)
description_entry = tk.Entry(form_frame, width=40)
description_entry.grid(row=4, column=1)

# Buttons
action_frame = tk.Frame(root)
action_frame.pack(pady=10)

tk.Button(action_frame, text="Save Medicine", command=save_data, bg="blue", fg="white", width=18).grid(row=0, column=0, padx=10)
tk.Button(action_frame, text="Delete Selected", command=delete_selected, bg="red", fg="white", width=18).grid(row=0, column=1, padx=10)

# Table
tk.Label(root, text="Saved Medicines").pack()

columns = ("Name", "Dosage", "Quantity", "Expiry", "Description")
table = ttk.Treeview(root, columns=columns, show="headings", height=8)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)
table.pack(pady=10)

# Bottom Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="View Medicine", command=view_medicine).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="View Summary", command=view_summary).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Exit", command=root.destroy).grid(row=0, column=2, padx=10)

# Initial Load
load_data()
check_alerts()

root.mainloop()
