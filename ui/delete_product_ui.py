import tkinter as tk
from tkinter import messagebox
from product import delete_product

def show_delete_product_menu():
    # Create a new window for deleting a product
    delete_window = tk.Toplevel()
    delete_window.title("Delete Product")
    delete_window.geometry("400x250")
    delete_window.configure(bg="#2c3e50")

    # Set fonts and colors
    label_font = ("Helvetica", 16, "bold")
    entry_font = ("Helvetica", 12)
    button_font = ("Helvetica", 12, "bold")

    # Label for window header
    header_label = tk.Label(delete_window, text="Delete Product", font=label_font, bg="#2c3e50", fg="#ecf0f1")
    header_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Product ID prompt and entry box
    product_id_label = tk.Label(delete_window, text="Enter Product ID:", font=entry_font, bg="#2c3e50", fg="#ecf0f1")
    product_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    product_id_entry = tk.Entry(delete_window, font=entry_font, width=20)
    product_id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Function to handle product deletion
    def handle_delete_product():
        try:
            product_id = int(product_id_entry.get())
            if product_id <= 0:
                raise ValueError("Invalid Product ID")
            delete_product(product_id)  # Perform the deletion action
            messagebox.showinfo("Success", "Product deleted successfully!")
            delete_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Product ID.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Delete Product button
    delete_button = tk.Button(delete_window, text="Delete Product", font=button_font, bg="#e74c3c", fg="#ffffff",
                              bd=0, padx=20, pady=10, relief=tk.FLAT, command=handle_delete_product)
    delete_button.grid(row=2, column=0, columnspan=2, pady=20)

    # Cancel button to close the window without deletion
    cancel_button = tk.Button(delete_window, text="Cancel", font=button_font, bg="#34495e", fg="#ffffff",
                              bd=0, padx=20, pady=10, relief=tk.FLAT, command=delete_window.destroy)
    cancel_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Adjust column layout
    delete_window.grid_columnconfigure(0, weight=1)
    delete_window.grid_columnconfigure(1, weight=1)
