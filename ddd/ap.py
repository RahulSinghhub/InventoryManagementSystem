import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='inventory_db',
        user='root',
        password='1234'
    )

# Function to authenticate user
def login(username, password):
    return username == "admin" and password == "1234"

# Function to add a new product
def add_product(name, category, stock_quantity, price):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, category, stock_quantity, price) VALUES (%s, %s, %s, %s)",
                   (name, category, stock_quantity, price))
    connection.commit()
    cursor.close()
    connection.close()
    messagebox.showinfo("Success", f"Product '{name}' added successfully.")

# Function to update product details
def update_product(product_id, name=None, category=None, stock_quantity=None, price=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    updates = []
    params = []

    if name is not None:
        updates.append("name = %s")
        params.append(name)
    if category is not None:
        updates.append("category = %s")
        params.append(category)
    if stock_quantity is not None:
        updates.append("stock_quantity = %s")
        params.append(stock_quantity)
    if price is not None:
        updates.append("price = %s")
        params.append(price)

    if updates:
        sql = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
        params.append(product_id)
        cursor.execute(sql, tuple(params))
        connection.commit()
        messagebox.showinfo("Success", f"Product ID {product_id} updated successfully.")
    else:
        messagebox.showwarning("Warning", "No updates provided.")

    cursor.close()
    connection.close()

# Function to update product quantity
def update_stock(product_id, quantity):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Update stock and log the sale
    cursor.execute("UPDATE products SET stock_quantity = stock_quantity + %s WHERE id = %s", (quantity, product_id))
    
    # Log the sale
    cursor.execute("INSERT INTO sales (product_id, quantity, sale_date) VALUES (%s, %s, NOW())", (product_id, quantity))
    
    connection.commit()
    cursor.close()
    connection.close()
    messagebox.showinfo("Success", f"Stock updated for product ID {product_id}.")

# Function to check low stock levels
def check_low_stock(threshold=10):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name, stock_quantity FROM products WHERE stock_quantity < %s", (threshold,))
    low_stock_products = cursor.fetchall()
    cursor.close()
    connection.close()

    if low_stock_products:
        alert_message = "Low Stock Alert!\n"
        for product in low_stock_products:
            alert_message += f"Product: {product[0]}, Stock: {product[1]}\n"
        messagebox.showwarning("Low Stock", alert_message)
    else:
        messagebox.showinfo("Info", "All products have sufficient stock.")

# Function to display the dashboard
def display_dashboard():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, category, stock_quantity, price FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()

    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Inventory Dashboard")
    
    dashboard_text = tk.Text(dashboard_window, width=70, height=15)
    dashboard_text.pack()

    dashboard_text.insert(tk.END, f"{'ID':<5} {'Name':<20} {'Category':<15} {'Stock':<10} {'Price':<10}\n")
    dashboard_text.insert(tk.END, "-" * 70 + "\n")
    for product in products:
        dashboard_text.insert(tk.END, f"{product[0]:<5} {product[1]:<20} {product[2]:<15} {product[3]:<10} {product[4]:<10.2f}\n")
    dashboard_text.insert(tk.END, "-" * 70 + "\n")

# Function to handle login
def handle_login():
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:", show='*')
    
    if login(username, password):
        messagebox.showinfo("Login", "Login successful!")
        show_main_menu()
    else:
        messagebox.showerror("Login", "Invalid username or password.")

# Function to show the main menu
def show_main_menu():
    main_menu_window = tk.Toplevel(root)
    main_menu_window.title("Main Menu")

    tk.Button(main_menu_window, text="Add Product", command=add_product_gui).pack(pady=10)
    tk.Button(main_menu_window, text="Update Stock", command=update_stock_gui).pack(pady=10)
    tk.Button(main_menu_window, text="Check Low Stock", command=check_low_stock).pack(pady=10)
    tk.Button(main_menu_window, text="View Dashboard", command=display_dashboard).pack(pady=10)
    tk.Button(main_menu_window, text="Generate Sales Report", command=generate_sales_report).pack(pady=10)
    tk.Button(main_menu_window, text="Exit", command=root.quit).pack(pady=10)

# Function to get product details from user to add
def add_product_gui():
    name = simpledialog.askstring("Add Product", "Enter product name:")
    category = simpledialog.askstring("Add Product", "Enter product category:")
    stock_quantity = simpledialog.askinteger("Add Product", "Enter stock quantity:")
    price = simpledialog.askfloat("Add Product", "Enter product price:")
    
    if name and category and stock_quantity is not None and price is not None:
        add_product(name, category, stock_quantity, price)

# Function to get product details from user to update stock
def update_stock_gui():
    product_id = simpledialog.askinteger("Update Stock", "Enter product ID:")
    quantity = simpledialog.askinteger("Update Stock", "Enter quantity to add (use negative number to reduce):")
    
    if product_id is not None and quantity is not None:
        update_stock(product_id, quantity)

# Function to generate and display sales report
def generate_sales_report():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get the top 5 best-selling products in the last week
    cursor.execute("""
        SELECT p.name, SUM(s.quantity) as total_sales, p.stock_quantity
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE s.sale_date >= NOW() - INTERVAL 7 DAY
        GROUP BY p.id
        ORDER BY total_sales DESC
        LIMIT 5
    """)
    
    sales_data = cursor.fetchall()
    cursor.close()
    connection.close()

    if sales_data:
        names = [row[0] for row in sales_data]
        total_sales = [row[1] for row in sales_data]
        stock_levels = [row[2] for row in sales_data]

        plt.figure(figsize=(10, 5))
        plt.bar(names, total_sales, color='blue', alpha=0.7, label='Total Sales')
        plt.xticks(rotation=45)
        
        for i, stock in enumerate(stock_levels):
            plt.text(i, total_sales[i] + 0.5, f'Stock: {stock}', ha='center')

        plt.title('Top 5 Best-Selling Products (Last Week)')
        plt.xlabel('Product Names')
        plt.ylabel('Total Sales')
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Sales Report", "No sales data available for the last week.")

# Main application window
root = tk.Tk()
root.title("Inventory Management System")
root.withdraw()  # Hide the main window initially

# Login on start
handle_login()

root.mainloop()