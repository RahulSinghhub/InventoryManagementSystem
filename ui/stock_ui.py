import tkinter as tk
from tkinter import messagebox
from product import update_product

def show_stock_menu():
    # Create a new window for updating stock
    stock_menu = tk.Toplevel()
    stock_menu.title("Update Stock")
    stock_menu.geometry("300x200")

    tk.Label(stock_menu, text="Product ID:").pack(pady=5)
    product_id_entry = tk.Entry(stock_menu)
    product_id_entry.pack(pady=5)

    tk.Label(stock_menu, text="New Stock Quantity:").pack(pady=5)
    stock_quantity_entry = tk.Entry(stock_menu)
    stock_quantity_entry.pack(pady=5)

    # Update stock button
    def handle_update_stock():
        product_id = int(product_id_entry.get())
        new_stock = int(stock_quantity_entry.get())
        update_product(product_id, stock_quantity=new_stock)
        messagebox.showinfo("Success", "Stock updated successfully!")
        stock_menu.destroy()

    tk.Button(stock_menu, text="Update Stock", command=handle_update_stock).pack(pady=10)
