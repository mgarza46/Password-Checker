import re
import random
import string
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


logging.basicConfig(filename='password_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def is_strong_password(password):
    feedback = []
    if len(password) < 8:
        feedback.append("must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        feedback.append("must include at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        feedback.append("must include at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        feedback.append("must include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        feedback.append("must include at least one special character.")
    
    common_patterns = ["123456", "password", "ABCDE1234", "abc123"]
    if any(pattern in password for pattern in common_patterns):
        feedback.append("Not strong enough! Try Again!")
    
    
    strength = get_password_strength(password)
    
    if feedback:
        return False, "Password " + ", ".join(feedback), strength
    return True, "Password is Strong!", strength

def get_password_strength(password):
    """ Return a strength rating based on length and complexity """
    score = 0
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"

def log_password_attempt(password, result, strength):
    logging.info(f"Password: '{password}' - Result: {result} - Strength: {strength}")

def generate_password(length=10):
    if length < 10:
        length = 10
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

def check_password():
    password = password_entry.get()
    is_valid, message, strength = is_strong_password(password)
    messagebox.showinfo("Password Check", message)
    log_password_attempt(password, message, strength)
    password_display_label.config(text=f"Entered Password: {password} - Strength: {strength}")
    update_strength_indicator(strength)

def generate_password_gui():
    new_password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, new_password)
    password_display_label.config(text=f"Generated Password: {new_password}")
    messagebox.showinfo("Generated Password", f"Your new password: {new_password}")
    update_strength_indicator("N/A")

def update_check_button_state(*args):
    if password_entry.get():
        check_button.config(state=tk.NORMAL)
    else:
        check_button.config(state=tk.DISABLED)

def update_strength_indicator(strength):
    if strength == "Weak":
        strength_indicator.config(value=25)
        strength_label.config(text="Weak", fg="red")
    elif strength == "Medium":
        strength_indicator.config(value=50)
        strength_label.config(text="Medium", fg="orange")
    elif strength == "Strong":
        strength_indicator.config(value=75)
        strength_label.config(text="Strong", fg="green")
    else:
        strength_indicator.config(value=0)
        strength_label.config(text="No password entered", fg="black")

def copy_to_clipboard():
    password = password_entry.get()
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()  # Keeps the clipboard updated immediately
    messagebox.showinfo("Copied to Clipboard", "Password copied to clipboard!")

root = tk.Tk()
root.title("Check how strong your password is!")
label = tk.Label(root, text="Enter password:")
label.pack()
password_entry = tk.Entry(root, show='*')
password_entry.pack()
password_entry.bind("<KeyRelease>", update_check_button_state)

password_display_label = tk.Label(root, text="")
password_display_label.pack()

strength_indicator = ttk.Progressbar(root, length=200, maximum=100, mode='determinate')
strength_indicator.pack(pady=10)

strength_label = tk.Label(root, text="No password entered", fg="black")
strength_label.pack()

check_button = tk.Button(root, text="Check Password", command=check_password, state=tk.DISABLED)
check_button.pack()
generate_button = tk.Button(root, text="Generate a password for me", command=generate_password_gui)
generate_button.pack()

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack()

root.mainloop()
