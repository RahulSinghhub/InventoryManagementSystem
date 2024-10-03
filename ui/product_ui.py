import tkinter as tk
from tkinter import ttk, messagebox
from product import add_product, update_product, delete_product, get_low_stock_products
from config import get_db_connection

# Function to show the product management menu
def show_product_menu():
    # Create a new window for managing products
    product_menu = tk.Toplevel()
    product_menu.title("Manage Products")
    product_menu.geometry("400x400")
    product_menu.configure(bg="#ecf0f1")

    # Set fonts and colors
    label_font = ("Helvetica", 12)
    entry_font = ("Helvetica", 12)
    button_font = ("Helvetica", 12, "bold")

    # Labels and entries for product details
    tk.Label(product_menu, text="Product Name:", font=label_font, bg="#ecf0f1").pack(pady=5)
    product_name = tk.Entry(product_menu, font=entry_font, width=30, bd=2, relief=tk.GROOVE)
    product_name.pack(pady=5)

    tk.Label(product_menu, text="Category:", font=label_font, bg="#ecf0f1").pack(pady=5)
    product_category = tk.Entry(product_menu, font=entry_font, width=30, bd=2, relief=tk.GROOVE)
    product_category.pack(pady=5)

    tk.Label(product_menu, text="Stock Quantity:", font=label_font, bg="#ecf0f1").pack(pady=5)
    product_quantity = tk.Entry(product_menu, font=entry_font, width=30, bd=2, relief=tk.GROOVE)
    product_quantity.pack(pady=5)

    tk.Label(product_menu, text="Price:", font=label_font, bg="#ecf0f1").pack(pady=5)
    product_price = tk.Entry(product_menu, font=entry_font, width=30, bd=2, relief=tk.GROOVE)
    product_price.pack(pady=5)

    # Add product button with rounded corners
    def handle_add_product():
        name = product_name.get()
        category = product_category.get()
        stock = int(product_quantity.get())
        price = float(product_price.get())
        add_product(name, category, stock, price)
        messagebox.showinfo("Success", "Product added successfully!")
        product_menu.destroy()

    add_button = tk.Button(product_menu, text="Add Product", command=handle_add_product, font=button_font, width=20, height=2, bg="#27ae60", fg="#ffffff", bd=0, relief="solid")
    add_button.pack(pady=20)

# Function to show the products in a structured table
def show_products_table(root):
    # Create a new window for showing products
    products_window = tk.Toplevel(root)
    products_window.title("Products")
    products_window.geometry("600x400")
    products_window.configure(bg="#ecf0f1")

    # Table header label
    tk.Label(products_window, text="Product List", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ffffff").pack(pady=10)

    # Treeview for displaying products
    tree = ttk.Treeview(products_window, columns=("ID", "Name", "Stock", "Total Sales"), show='headings', height=10)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Stock", text="Stock Quantity")
    tree.heading("Total Sales", text="Total Sales")

    # Styling the Treeview
    tree.tag_configure('evenrow', background="#f0f0f0")
    tree.tag_configure('oddrow', background="#ffffff")
    
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Fetch product details and insert into the treeview
    query = """
    SELECT p.id, p.name, p.stock_quantity, COALESCE(SUM(s.quantity), 0) AS total_sales
    FROM products p
    LEFT JOIN sales s ON p.id = s.product_id
    GROUP BY p.id;
    """

    try:
        connection = get_db_connection()  # Adjust as per your DB connection setup
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert("", tk.END, values=row, tags=(tag,))

    except Exception as e:
        print(f"Error fetching products: {e}")
    finally:
        cursor.close()
        connection.close()

# Function to show low stock products
def show_low_stock():
    low_stock_products = get_low_stock_products()
    low_stock_window = tk.Toplevel()
    low_stock_window.title("Low Stock Products")
    low_stock_window.geometry("400x300")
    low_stock_window.configure(bg="#ecf0f1")

    tk.Label(low_stock_window, text="Low Stock Products", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ffffff").pack(pady=10)

    # Structured display of low stock products
    for product in low_stock_products:
        product_text = f"ID: {product['id']} | Name: {product['name']} | Stock: {product['stock_quantity']}"
        tk.Label(low_stock_window, text=product_text, font=("Helvetica", 12), bg="#ecf0f1").pack(pady=2)

    # Close button
    close_button = tk.Button(low_stock_window, text="Close", command=low_stock_window.destroy, bg="#c0392b", fg="#ffffff", font=("Helvetica", 12), padx=10, pady=5)
    close_button.pack(pady=20)

