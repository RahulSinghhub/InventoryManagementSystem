import tkinter as tk
from tkinter import messagebox
from ui.product_ui import show_product_menu, show_products_table
from ui.stock_ui import show_stock_menu
from ui.report_ui import show_report_menu
from ui.delete_product_ui import show_delete_product_menu
from ui.prediction_ui import show_predictions


def show_main_menu(root):
    # Create the main menu window
    main_menu = tk.Toplevel(root)
    main_menu.title("Inventory Management System - Main Menu")
    main_menu.geometry("600x400")
    main_menu.configure(bg="#2c3e50")  # Dark background

    # Set fonts and colors
    label_font = ("Helvetica", 16, "bold")
    button_font = ("Helvetica", 12, "bold")

    # Inventory Management System label
    main_label = tk.Label(main_menu, text="Inventory Management System", font=label_font, bg="#2c3e50", fg="#ecf0f1")
    main_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Function to create rounded buttons without icons
    def create_button(parent, text, command, row, column):
        # Create button with text
        button = tk.Button(parent, text=text, font=button_font,
                           bg="#27ae60", fg="#ffffff", bd=0, padx=20, pady=10,
                           relief=tk.GROOVE, width=15)
        button.config(command=command)
        button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    # Add buttons for different functionalities
    create_button(main_menu, "Add Product", show_product_menu, row=1, column=0)
    create_button(main_menu, "Update Stock", show_stock_menu, row=1, column=1)
    create_button(main_menu, "View Products", lambda: show_products_table(root), row=2, column=0)
    create_button(main_menu, "View Sales Graph", show_report_menu, row=2, column=1)
    create_button(main_menu, "Delete Product", show_delete_product_menu, row=3, column=0)
    create_button(main_menu, "Stock Predictions", show_predictions, row=3, column=1)

    # Exit button at the bottom, with a different color
    exit_button = tk.Button(main_menu, text="Exit", font=button_font, bg="#c0392b", fg="#ffffff", bd=0,
                            padx=20, pady=10, command=main_menu.quit)
    exit_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Adjust grid columns for responsiveness
    main_menu.grid_columnconfigure(0, weight=1)
    main_menu.grid_columnconfigure(1, weight=1)


# This is to prevent access without login
if __name__ == "__main__":
    messagebox.showerror("Error", "You must log in first to access the main menu.")


def logout(root, main_menu_window):
    main_menu_window.destroy()  # Close the main menu window
    root.deiconify()
