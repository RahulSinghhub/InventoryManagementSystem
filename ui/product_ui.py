import tkinter as tk
from tkinter import messagebox
from product import add_product, update_product

def show_product_menu():
    # Create a new window for managing products
    product_menu = tk.Toplevel()
    product_menu.title("Manage Products")
    product_menu.geometry("300x300")

    tk.Label(product_menu, text="Product Name:").pack(pady=5)
    product_name = tk.Entry(product_menu)
    product_name.pack(pady=5)

    tk.Label(product_menu, text="Category:").pack(pady=5)
    product_category = tk.Entry(product_menu)
    product_category.pack(pady=5)

    tk.Label(product_menu, text="Stock Quantity:").pack(pady=5)
    product_quantity = tk.Entry(product_menu)
    product_quantity.pack(pady=5)

    tk.Label(product_menu, text="Price:").pack(pady=5)
    product_price = tk.Entry(product_menu)
    product_price.pack(pady=5)

    # Add product button
    def handle_add_product():
        name = product_name.get()
        category = product_category.get()
        stock = int(product_quantity.get())
        price = float(product_price.get())
        add_product(name, category, stock, price)
        messagebox.showinfo("Success", "Product added successfully!")
        product_menu.destroy()

    tk.Button(product_menu, text="Add Product", command=handle_add_product).pack(pady=10)

    # Update product button (asks for product ID)
    tk.Label(product_menu, text="Product ID to update:").pack(pady=5)
    product_id_entry = tk.Entry(product_menu)
    product_id_entry.pack(pady=5)

    def handle_update_product():
        product_id = int(product_id_entry.get())
        name = product_name.get() or None
        category = product_category.get() or None
        stock = int(product_quantity.get()) if product_quantity.get() else None
        price = float(product_price.get()) if product_price.get() else None
        update_product(product_id, name, category, stock, price)
        messagebox.showinfo("Success", "Product updated successfully!")
        product_menu.destroy()

    tk.Button(product_menu, text="Update Product", command=handle_update_product).pack(pady=10)
