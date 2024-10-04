import tkinter as tk
from tkinter import messagebox
from config import get_db_connection  # Assuming your DB connection method is here
from datetime import datetime, timedelta
import random
from decimal import Decimal

def simulate_sales_for_all_products():
    # Simulate sales for each product by calculating moving averages for all previous sales
    connection = get_db_connection()
    cursor = connection.cursor()

    # Step 1: Get all products
    cursor.execute("SELECT id FROM products")
    products = cursor.fetchall()

    for product in products:
        product_id = product[0]

        # Step 2: Get the latest sale date for each product
        cursor.execute("""
            SELECT MAX(sale_date)
            FROM sales
            WHERE product_id = %s
        """, (product_id,))
        latest_sale_date = cursor.fetchone()[0]

        if latest_sale_date is None:
            latest_sale_date = datetime.now() - timedelta(days=30)  # Assume no sales, simulate from 30 days ago

        # Step 3: Simulate sales from the next day after the last sale date until today
        today = datetime.now()
        delta = today - latest_sale_date

        for day in range(1, delta.days + 1):
            current_date = latest_sale_date + timedelta(days=day)

            # Step 4: Calculate average sales for the product
            cursor.execute("""
                SELECT AVG(quantity) 
                FROM sales 
                WHERE product_id = %s
            """, (product_id,))
            avg_sales = cursor.fetchone()[0]
            if avg_sales is None:
                avg_sales = Decimal(5)  # Default to 5 units if no sales history

            # Step 5: Generate a random sales quantity within a range (20% variation)
            simulated_sales = int(float(avg_sales) * random.uniform(0.8, 1.2))

            # Step 6: Insert simulated sales into the sales table
            cursor.execute("""
                INSERT INTO sales (product_id, quantity, sale_date)
                VALUES (%s, %s, %s)
            """, (product_id, simulated_sales, current_date))

            # Step 7: Update the stock quantity in the products table
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = stock_quantity - %s
                WHERE id = %s
            """, (simulated_sales, product_id))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

    messagebox.showinfo("Simulation Complete", "Sales simulation completed successfully!")


def show_simulate_sales_menu():
    # Create a new window for simulating sales
    simulate_window = tk.Toplevel()
    simulate_window.title("Simulate Sales")
    simulate_window.geometry("400x200")
    simulate_window.configure(bg="#2c3e50")

    # Label and message to confirm simulation
    label_font = ("Helvetica", 14, "bold")
    message_font = ("Helvetica", 12)
    tk.Label(simulate_window, text="Simulate Sales", font=label_font, bg="#2c3e50", fg="#ecf0f1").pack(pady=20)
    tk.Label(simulate_window, text="This will simulate sales for all products.\nAre you sure you want to proceed?",
             font=message_font, bg="#2c3e50", fg="#ecf0f1").pack(pady=10)

    # Confirmation button
    def confirm_simulation():
        simulate_sales_for_all_products()  # Call the sales simulation function
        simulate_window.destroy()  # Close the window after simulation

    tk.Button(simulate_window, text="Confirm", font=("Helvetica", 12, "bold"), bg="#27ae60", fg="#ffffff", bd=0,
              padx=20, pady=10, relief=tk.FLAT, command=confirm_simulation).pack(pady=20)

    # Cancel button
    tk.Button(simulate_window, text="Cancel", font=("Helvetica", 12, "bold"), bg="#c0392b", fg="#ffffff", bd=0,
              padx=20, pady=10, relief=tk.FLAT, command=simulate_window.destroy).pack(pady=10)
