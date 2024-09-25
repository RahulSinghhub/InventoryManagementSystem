import tkinter as tk
from tkinter import messagebox
from product import delete_product

def show_delete_product_menu():
    # Create a new window for deleting a product
    delete_window = tk.Toplevel()
    delete_window.title("Delete Product")
    delete_window.geometry("300x200")

    tk.Label(delete_window, text="Enter Product ID to delete:").pack(pady=10)
    product_id_entry = tk.Entry(delete_window)
    product_id_entry.pack(pady=5)

    def handle_delete_product():
        product_id = int(product_id_entry.get())
        delete_product(product_id)
        messagebox.showinfo("Success", "Product deleted successfully!")
        delete_window.destroy()

    tk.Button(delete_window, text="Delete Product", command=handle_delete_product).pack(pady=10)
