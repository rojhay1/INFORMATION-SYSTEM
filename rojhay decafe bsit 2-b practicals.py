import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ============================================================
# DATABASE
# ============================================================

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    position TEXT NOT NULL
)
""")

conn.commit()


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()
window.title("Employee Profile")
window.geometry("650x500")
window.resizable(False, False)


# ============================================================
# COLORS - BLUE THEME
# ============================================================

BG_COLOR = "#D6EAF8"
TITLE_COLOR = "#154360"
BUTTON_COLOR = "#2874A6"
TEXT_COLOR = "#FFFFFF"
ENTRY_BG = "#FFFFFF"
TABLE_HEADER = "#21618C"

window.configure(bg=BG_COLOR)


# ============================================================
# VARIABLES
# ============================================================

name_var = tk.StringVar()
age_var = tk.StringVar()
position_var = tk.StringVar()


# ============================================================
# FUNCTIONS
# ============================================================

def clear_fields():
    name_var.set("")
    age_var.set("")
    position_var.set("")

    selected = employee_table.selection()

    if selected:
        employee_table.selection_remove(selected)


def display_employees():
    for item in employee_table.get_children():
        employee_table.delete(item)

    cursor.execute("""
        SELECT id, name, age, position
        FROM employees
        ORDER BY id
    """)

    employees = cursor.fetchall()

    for employee in employees:
        employee_table.insert(
            "",
            tk.END,
            values=(employee[1], employee[2], employee[3]),
            tags=(str(employee[0]),)
        )


def add_employee():
    name = name_var.get().strip()
    age = age_var.get().strip()
    position = position_var.get().strip()

    if name == "" or age == "" or position == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute("""
        INSERT INTO employees (name, age, position)
        VALUES (?, ?, ?)
    """, (name, age, position))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Employee added successfully!"
    )

    clear_fields()
    display_employees()


def select_employee(event):
    selected = employee_table.selection()

    if selected:
        item = employee_table.item(selected[0])
        values = item["values"]

        name_var.set(values[0])
        age_var.set(values[1])
        position_var.set(values[2])


def update_employee():
    selected = employee_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an employee to update."
        )
        return

    # Get hidden database ID from table tag
    item = employee_table.item(selected[0])
    employee_id = item["tags"][0]

    name = name_var.get().strip()
    age = age_var.get().strip()
    position = position_var.get().strip()

    if name == "" or age == "" or position == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute("""
        UPDATE employees
        SET name = ?, age = ?, position = ?
        WHERE id = ?
    """, (name, age, position, employee_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Employee updated successfully!"
    )

    clear_fields()
    display_employees()


def delete_employee():
    selected = employee_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an employee to delete."
        )
        return

    # Get hidden database ID
    item = employee_table.item(selected[0])
    employee_id = item["tags"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this employee?"
    )

    if confirm:

        cursor.execute(
            "DELETE FROM employees WHERE id = ?",
            (employee_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Employee deleted successfully!"
        )

        clear_fields()
        display_employees()


def exit_program():
    confirm = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if confirm:
        conn.close()
        window.destroy()


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    window,
    text="Employee Profile",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title_label.pack(pady=15)


# ============================================================
# INPUT FRAME
# ============================================================

input_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

input_frame.pack(pady=5)


# ============================================================
# EMPLOYEE NAME
# ============================================================

tk.Label(
    input_frame,
    text="Employee Name:",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=TITLE_COLOR
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

name_entry = tk.Entry(
    input_frame,
    textvariable=name_var,
    width=35,
    bg=ENTRY_BG
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# ============================================================
# AGE
# ============================================================

tk.Label(
    input_frame,
    text="Age:",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=TITLE_COLOR
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

age_entry = tk.Entry(
    input_frame,
    textvariable=age_var,
    width=35,
    bg=ENTRY_BG
)

age_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# ============================================================
# POSITION
# ============================================================

tk.Label(
    input_frame,
    text="Position:",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=TITLE_COLOR
).grid(
    row=2,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

position_entry = tk.Entry(
    input_frame,
    textvariable=position_var,
    width=35,
    bg=ENTRY_BG
)

position_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

button_frame.pack(pady=10)


# ============================================================
# BUTTONS
# ============================================================

add_button = tk.Button(
    button_frame,
    text="Add",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    activebackground=TABLE_HEADER,
    activeforeground=TEXT_COLOR,
    command=add_employee
)

add_button.grid(row=0, column=0, padx=5)


update_button = tk.Button(
    button_frame,
    text="Update",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    activebackground=TABLE_HEADER,
    activeforeground=TEXT_COLOR,
    command=update_employee
)

update_button.grid(row=0, column=1, padx=5)


delete_button = tk.Button(
    button_frame,
    text="Delete",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    activebackground=TABLE_HEADER,
    activeforeground=TEXT_COLOR,
    command=delete_employee
)

delete_button.grid(row=0, column=2, padx=5)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    activebackground=TABLE_HEADER,
    activeforeground=TEXT_COLOR,
    command=clear_fields
)

clear_button.grid(row=0, column=3, padx=5)


exit_button = tk.Button(
    button_frame,
    text="Exit",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    activebackground=TABLE_HEADER,
    activeforeground=TEXT_COLOR,
    command=exit_program
)

exit_button.grid(row=0, column=4, padx=5)


# ============================================================
# EMPLOYEE INFORMATION
# ============================================================

info_label = tk.Label(
    window,
    text="Employee Information",
    font=("Arial", 14, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

info_label.pack(pady=(10, 5))


# ============================================================
# TABLE STYLE
# ============================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#FFFFFF",
    foreground="#154360",
    rowheight=25,
    fieldbackground="#FFFFFF",
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=TABLE_HEADER,
    foreground="#FFFFFF",
    font=("Arial", 10, "bold")
)

style.map(
    "Treeview",
    background=[
        ("selected", "#5DADE2")
    ],
    foreground=[
        ("selected", "#FFFFFF")
    ]
)


# ============================================================
# EMPLOYEE TABLE
# ============================================================

table_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

table_frame.pack(pady=5)

employee_table = ttk.Treeview(
    table_frame,
    columns=("Name", "Age", "Position"),
    show="headings",
    height=8
)


# ============================================================
# TABLE HEADINGS
# ============================================================

employee_table.heading(
    "Name",
    text="Name"
)

employee_table.heading(
    "Age",
    text="Age"
)

employee_table.heading(
    "Position",
    text="Position"
)


# ============================================================
# TABLE COLUMNS
# ============================================================

employee_table.column(
    "Name",
    width=220
)

employee_table.column(
    "Age",
    width=100,
    anchor="center"
)

employee_table.column(
    "Position",
    width=220
)

employee_table.pack()


# ============================================================
# EVENT HANDLING
# ============================================================

employee_table.bind(
    "<<TreeviewSelect>>",
    select_employee
)


# ============================================================
# DISPLAY DATABASE RECORDS
# ============================================================

display_employees()


# ============================================================
# RUN APPLICATION
# ============================================================

window.mainloop()
