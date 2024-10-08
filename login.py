import tkinter as tk
from tkinter import messagebox
from ui.main_menu import show_main_menu

# Hardcoded admin credentials
ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}

def login_screen():
    # Create a single Tk root window
    root = tk.Tk()
    root.title("Admin Login")
    root.geometry("400x300")
    root.configure(bg="#2c3e50")

    # Set fonts and colors
    entry_font = ("Helvetica", 12)
    button_font = ("Helvetica", 12, "bold")
    label_font = ("Helvetica", 16, "bold")

    # Admin Login label
    login_label = tk.Label(root, text="Admin Login", font=label_font, bg="#2c3e50", fg="#ecf0f1")
    login_label.pack(pady=20)

    # Placeholder functions for username and password
    def set_placeholder(entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')

    def clear_placeholder(event, entry, placeholder_text):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def add_placeholder(event, entry, placeholder_text):
        if not entry.get():
            set_placeholder(entry, placeholder_text)

    # Username entry with placeholder
    username_entry = tk.Entry(root, font=entry_font, width=30, bd=2, relief=tk.GROOVE)
    username_placeholder = "Username"
    set_placeholder(username_entry, username_placeholder)
    username_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, username_entry, username_placeholder))
    username_entry.bind("<FocusOut>", lambda event: add_placeholder(event, username_entry, username_placeholder))
    username_entry.pack(pady=10)

    # Password entry with placeholder
    password_entry = tk.Entry(root, font=entry_font, width=30, bd=2, relief=tk.GROOVE, show="*")
    password_placeholder = "Password"
    set_placeholder(password_entry, password_placeholder)
    password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, password_entry, password_placeholder))
    password_entry.bind("<FocusOut>", lambda event: add_placeholder(event, password_entry, password_placeholder))
    password_entry.pack(pady=10)

    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            # Customize the success message box with more user-friendly info
            messagebox.showinfo("Login Successful", "Welcome, Admin! You are now logged in.")

            # Clear the login window and show the main menu in the same window
            root.withdraw()  # Hide the login window
            show_main_menu(root)  # Show the main menu in the same root window
        else:
            # Customize the error message box for a better user experience
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    # Login button with slightly smaller size and padding
    login_button = tk.Button(
        root, 
        text="Login", 
        command=verify_login, 
        font=button_font, 
        width=17,    # Reduced width
        height=2,    # Reduced height
        bg="#27ae60", 
        fg="#ffffff", 
        bd=0, 
        padx=10,     # Reduced padding
        pady=5       # Reduced padding
    )
    login_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    login_screen()
