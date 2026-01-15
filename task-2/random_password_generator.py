import tkinter as tk
from tkinter import messagebox
import secrets
import string

# ---------------- PASSWORD LOGIC ----------------
def generate_password():
    try:
        length = int(length_entry.get())

        if length < 8 or length > 50:
            raise ValueError("Length out of range")

        chars = ""

        if lower_var.get():
            chars += string.ascii_lowercase
        if upper_var.get():
            chars += string.ascii_uppercase
        if digit_var.get():
            chars += string.digits
        if symbol_var.get():
            chars += string.punctuation

        if not chars:
            raise ValueError("No character set selected")

        exclude = exclude_entry.get()
        chars = ''.join(c for c in chars if c not in exclude)

        if not chars:
            raise ValueError("All characters excluded")

        # Enforce security rules
        password = [
            secrets.choice(string.ascii_lowercase) if lower_var.get() else "",
            secrets.choice(string.ascii_uppercase) if upper_var.get() else "",
            secrets.choice(string.digits) if digit_var.get() else "",
            secrets.choice(string.punctuation) if symbol_var.get() else ""
        ]

        password = [p for p in password if p]

        while len(password) < length:
            password.append(secrets.choice(chars))

        secrets.SystemRandom().shuffle(password)
        password = ''.join(password)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

    except ValueError as e:
        messagebox.showerror("Error", str(e))


# ---------------- CLIPBOARD ----------------
def copy_to_clipboard():
    pwd = password_entry.get()
    if pwd:
        root.clipboard_clear()
        root.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard")


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("420x520")
root.configure(bg="#f4f6f8")

main = tk.Frame(root, bg="white", bd=2, relief="groove")
main.pack(padx=20, pady=20, fill="both", expand=True)

tk.Label(
    main,
    text="Advanced Password Generator",
    font=("Arial", 16, "bold"),
    fg="#1a237e",
    bg="white"
).pack(pady=10)

# -------- LENGTH --------
tk.Label(main, text="Password Length (8–50)", bg="white").pack(anchor="w", padx=20)
length_entry = tk.Entry(main)
length_entry.pack(fill="x", padx=20, pady=5)
length_entry.insert(0, "12")

# -------- OPTIONS --------
lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

tk.Label(main, text="Character Options", bg="white",
         font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=5)

tk.Checkbutton(main, text="Lowercase Letters", variable=lower_var, bg="white").pack(anchor="w", padx=30)
tk.Checkbutton(main, text="Uppercase Letters", variable=upper_var, bg="white").pack(anchor="w", padx=30)
tk.Checkbutton(main, text="Numbers", variable=digit_var, bg="white").pack(anchor="w", padx=30)
tk.Checkbutton(main, text="Symbols", variable=symbol_var, bg="white").pack(anchor="w", padx=30)

# -------- EXCLUDE --------
tk.Label(main, text="Exclude Characters (optional)", bg="white").pack(anchor="w", padx=20)
exclude_entry = tk.Entry(main)
exclude_entry.pack(fill="x", padx=20, pady=5)

# -------- GENERATE --------
tk.Button(
    main,
    text="Generate Password",
    bg="#1e88e5",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=generate_password
).pack(pady=15)

# -------- RESULT --------
password_entry = tk.Entry(
    main,
    font=("Courier New", 12, "bold"),
    justify="center"
)
password_entry.pack(fill="x", padx=20, pady=5)

tk.Button(
    main,
    text="Copy to Clipboard",
    bg="#43a047",
    fg="white",
    relief="flat",
    command=copy_to_clipboard
).pack(pady=10)

root.mainloop()
