import tkinter as tk
from tkinter import messagebox
from ui.product_ui import show_product_menu,show_products_table
from ui.stock_ui import show_stock_menu
from ui.report_ui import show_report_menu
from ui.delete_product_ui import show_delete_product_menu


def show_main_menu(root):
    # Create the main menu window
    main_menu = tk.Toplevel(root)
    main_menu.title("Inventory Management System - Main Menu")
    main_menu.geometry("300x300")

    tk.Label(main_menu, text="Inventory Management System", font=("Arial", 14)).pack(pady=10)

    # Add buttons for different functionalities
    tk.Button(main_menu, text="Add Product", width=20, command=show_product_menu).pack(pady=5)
    tk.Button(main_menu, text="Update Stock", width=20, command=show_stock_menu).pack(pady=5)
    tk.Button(main_menu, text="View Products", width=20, command=lambda: show_products_table(root)).pack(pady=5)  # Pass root correctly
    tk.Button(main_menu, text="View Sales Graph", width=20, command=show_report_menu).pack(pady=5)
    tk.Button(main_menu, text="Delete Product", width=20, command=show_delete_product_menu).pack(pady=5)
    tk.Button(main_menu, text="Exit", width=20, command=main_menu.quit).pack(pady=20)


# This is to prevent access without login
if __name__ == "__main__":
    messagebox.showerror("Error", "You must log in first to access the main menu.")

def logout(root, main_menu_window):
    main_menu_window.destroy()  # Close the main menu window
    root.deiconify()