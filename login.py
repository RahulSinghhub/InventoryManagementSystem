import tkinter as tk
from tkinter import messagebox
from ui.main_menu import show_main_menu

# Hardcoded admin credentials
ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}

def login_screen():
    # Create a login window
    root = tk.Tk()
    root.title("Admin Login")
    root.geometry("300x200")

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")  
            main_root = tk.Tk()
            root.withdraw()  
            show_main_menu(main_root) 
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    tk.Button(root, text="Login", command=verify_login).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    login_screen()
