import tkinter as tk
from tkinter import messagebox
from config import get_db_connection

def show_add_sales_menu():
    # Create a new window for adding sales
    add_sales_menu = tk.Toplevel()
    add_sales_menu.title("Add Sales Entry")
    add_sales_menu.geometry("400x300")
    add_sales_menu.configure(bg="#2c3e50")  # Dark background

    # Set fonts and colors
    label_font = ("Helvetica", 12, "bold")
    entry_font = ("Helvetica", 12)

    # Labels and input fields for product_id and quantity
    product_id_label = tk.Label(add_sales_menu, text="Product ID:", font=label_font, bg="#2c3e50", fg="#ecf0f1")
    product_id_label.pack(pady=10)
    product_id_entry = tk.Entry(add_sales_menu, font=entry_font)
    product_id_entry.pack(pady=10)

    quantity_label = tk.Label(add_sales_menu, text="Quantity Sold:", font=label_font, bg="#2c3e50", fg="#ecf0f1")
    quantity_label.pack(pady=10)
    quantity_entry = tk.Entry(add_sales_menu, font=entry_font)
    quantity_entry.pack(pady=10)

    def add_sales_to_db():
        product_id = product_id_entry.get()
        quantity = quantity_entry.get()

        if not product_id or not quantity:
            messagebox.showerror("Input Error", "Please enter both Product ID and Quantity.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be an integer.")
            return

        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert new sales record into the sales table
            cursor.execute(
                """
                INSERT INTO sales (product_id, quantity, sale_date)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                """, (product_id, quantity)
            )

            # Update stock_quantity in the products table
            cursor.execute(
                """
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE id = %s
                """, (quantity, product_id)
            )

            connection.commit()  # Commit the transaction
            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Sales entry added and stock quantity updated.")
            add_sales_menu.destroy()  # Close the add sales window

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Submit button
    submit_button = tk.Button(add_sales_menu, text="Add Sales", font=label_font, bg="#27ae60", fg="#ffffff", padx=20, pady=10, command=add_sales_to_db)
    submit_button.pack(pady=20)

# To integrate this into the main menu, simply import this function and add the relevant button.
