
from ui.main_menu import show_main_menu
from database import setup_database
import tkinter as tk

# Setup database if not exists
setup_database()

# Main application window
root = tk.Tk()
root.title("Inventory Management System")
root.withdraw()  # Hide the main window initially

# Display main menu after login
show_main_menu(root)

root.mainloop()
