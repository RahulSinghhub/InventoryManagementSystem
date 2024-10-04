import tkinter as tk
from tkinter import messagebox
from product import update_product

def show_stock_menu():
    # Create a new window for updating stock
    stock_menu = tk.Toplevel()
    stock_menu.title("Update Stock")
    stock_menu.geometry("400x250")
    stock_menu.configure(bg="#2c3e50")

    # Set fonts and styles
    label_font = ("Helvetica", 14)
    entry_font = ("Helvetica", 12)
    button_font = ("Helvetica", 12, "bold")

    # Header Label
    header_label = tk.Label(stock_menu, text="Update Stock", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
    header_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Product ID label and entry
    product_id_label = tk.Label(stock_menu, text="Product ID:", font=label_font, bg="#2c3e50", fg="#ecf0f1")
    product_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    product_id_entry = tk.Entry(stock_menu, font=entry_font)
    product_id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # New Stock Quantity label and entry
    stock_quantity_label = tk.Label(stock_menu, text="New Stock Quantity:", font=label_font, bg="#2c3e50", fg="#ecf0f1")
    stock_quantity_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    stock_quantity_entry = tk.Entry(stock_menu, font=entry_font)
    stock_quantity_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Update Stock button functionality
    def handle_update_stock():
        try:
            product_id = int(product_id_entry.get())
            new_stock = int(stock_quantity_entry.get())
            if product_id <= 0 or new_stock < 0:
                raise ValueError("Invalid input values")
            update_product(product_id, stock_quantity=new_stock)
            messagebox.showinfo("Success", "Stock updated successfully!")
            stock_menu.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Update Stock button
    update_button = tk.Button(stock_menu, text="Update Stock", font=button_font, bg="#27ae60", fg="#ffffff", bd=0,
                              padx=20, pady=10, relief=tk.FLAT, command=handle_update_stock)
    update_button.grid(row=3, column=0, columnspan=2, pady=20)

    # Cancel button to close the window
    cancel_button = tk.Button(stock_menu, text="Cancel", font=button_font, bg="#34495e", fg="#ffffff", bd=0,
                              padx=20, pady=10, relief=tk.FLAT, command=stock_menu.destroy)
    cancel_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Adjust column layout
    stock_menu.grid_columnconfigure(0, weight=1)
    stock_menu.grid_columnconfigure(1, weight=1)
