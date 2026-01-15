import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------- INPUT VALIDATION ----------------
def only_numbers(value):
    if value == "":
        return True
    return value.replace(".", "", 1).isdigit()

def only_letters(value):
    if value == "":
        return True
    return value.replace(" ", "").isalpha()

#database
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    name TEXT,
    height REAL,
    weight REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

#logic
def calculate_bmi():
    try:
        name = name_entry.get().strip()
        height = float(height_entry.get()) / 100
        weight = float(weight_entry.get())

        if not name:
            raise ValueError

        if height <= 0 or weight <= 0:
            raise ValueError

        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(
            text=f"BMI: {bmi}  |  {category}",
            fg="#2e7d32"
        )

        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        cursor.execute(
            "INSERT INTO bmi_records VALUES (?, ?, ?, ?, ?, ?)",
            (name, height * 100, weight, bmi, category, date)
        )
        conn.commit()

        load_history()

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "• Name must contain only letters\n• Height & Weight must be numbers"
        )

#history
def load_history():
    history_list.delete(0, tk.END)
    name = name_entry.get().strip()

    cursor.execute(
        "SELECT bmi, category, date FROM bmi_records WHERE name=?",
        (name,)
    )
    rows = cursor.fetchall()

    for row in rows:
        history_list.insert(
            tk.END,
            f"{row[2]}  →  BMI {row[0]} ({row[1]})"
        )

#graph
def show_graph():
    name = name_entry.get().strip()
    cursor.execute(
        "SELECT bmi, date FROM bmi_records WHERE name=?",
        (name,)
    )
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("No Data", "No BMI records found")
        return

    bmi_values = [row[0] for row in data]
    dates = [row[1] for row in data]

    plt.figure()
    plt.plot(dates, bmi_values, marker="o")
    plt.xticks(rotation=45)
    plt.title(f"BMI Trend for {name}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.tight_layout()
    plt.show()

#tkinter gui application
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("500x600")
root.configure(bg="#f4f6f8")

num_vcmd = root.register(only_numbers)
name_vcmd = root.register(only_letters)

main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

tk.Label(
    main_frame,
    text="BMI Calculator",
    font=("Arial", 18, "bold"),
    bg="#ffffff",
    fg="#bd25b6"
).pack(pady=15)

# inputs
def labeled_entry(text, vcmd=None):
    tk.Label(
        main_frame,
        text=text,
        font=("Arial", 11),
        bg="#ffffff"
    ).pack(anchor="w", padx=30)

    entry = tk.Entry(
        main_frame,
        font=("Arial", 11),
        validate="key" if vcmd else "none",
        validatecommand=(vcmd, "%P") if vcmd else None
    )
    entry.pack(fill="x", padx=30, pady=5)
    return entry

name_entry = labeled_entry("Name", name_vcmd)
height_entry = labeled_entry("Height (cm)", num_vcmd)
weight_entry = labeled_entry("Weight (kg)", num_vcmd)

tk.Button(
    main_frame,
    text="Calculate BMI",
    font=("Arial", 11, "bold"),
    bg="#372339",
    fg="white",
    relief="flat",
    command=calculate_bmi
).pack(pady=15)

result_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 12, "bold"),
    bg="#ffffff"
)
result_label.pack()


tk.Label(
    main_frame,
    text="BMI History",
    font=("Arial", 13, "bold"),
    bg="#ffffff"
).pack(pady=10)

history_list = tk.Listbox(
    main_frame,
    height=8,
    font=("Arial", 10)
)
history_list.pack(fill="both", padx=30, pady=5)

tk.Button(
    main_frame,
    text="Show BMI Graph",
    font=("Arial", 11),
    bg="#d72121",
    fg="white",
    relief="flat",
    command=show_graph
).pack(pady=10)

root.mainloop()
conn.close()
0