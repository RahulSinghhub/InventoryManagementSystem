import tkinter as tk
from tkinter import messagebox
from ui.product_ui import show_product_menu
from ui.stock_ui import show_stock_menu
from ui.report_ui import show_report_menu

def show_main_menu(root):
    # Create the main window
    main_menu = tk.Toplevel(root)
    main_menu.title("Inventory Management System - Main Menu")
    main_menu.geometry("300x200")

    tk.Label(main_menu, text="Inventory Management System", font=("Arial", 14)).pack(pady=10)

    # Add buttons for different functionalities
    tk.Button(main_menu, text="Manage Products", width=20, command=show_product_menu).pack(pady=5)
    tk.Button(main_menu, text="Update Stock", width=20, command=show_stock_menu).pack(pady=5)
    tk.Button(main_menu, text="View Sales Report", width=20, command=show_report_menu).pack(pady=5)

    # Exit button
    tk.Button(main_menu, text="Exit", width=20, command=root.quit).pack(pady=20)
