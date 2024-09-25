import tkinter as tk
from tkinter import messagebox
from product import add_product, update_product, delete_product, get_low_stock_products
from config import get_db_connection

def show_product_menu():
    # Create a new window for managing products
    product_menu = tk.Toplevel()
    product_menu.title("Manage Products")
    product_menu.geometry("300x400")

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

# Function to show low stock products
def show_low_stock():
    low_stock_products = get_low_stock_products()
    low_stock_window = tk.Toplevel()
    low_stock_window.title("Low Stock Products")
    low_stock_window.geometry("400x300")
    tk.Label(low_stock_window, text="Low Stock Products", font=("Arial", 14)).pack(pady=10)
    
    for product in low_stock_products:
        tk.Label(low_stock_window, text=f"Product ID: {product['id']}, Name: {product['name']}, Stock: {product['stock_quantity']}").pac