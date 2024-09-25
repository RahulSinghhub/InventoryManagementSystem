from config import get_db_connection

# Function to add a product
def add_product(name, category, stock_quantity, price):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, category, stock_quantity, price) VALUES (%s, %s, %s, %s)",
                   (name, category, stock_quantity, price))
    connection.commit()
    cursor.close()
    connection.close()

# Function to update a product
def update_product(product_id, name=None, category=None, stock_quantity=None, price=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Prepare the update query dynamically based on non-null fields
    update_fields = []
    values = []

    if name:
        update_fields.append("name = %s")
        values.append(name)
    if category:
        update_fields.append("category = %s")
        values.append(category)
    if stock_quantity is not None:
        update_fields.append("stock_quantity = %s")
        values.append(stock_quantity)
    if price is not None:
        update_fields.append("price = %s")
        values.append(price)
    
    if update_fields:
        query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
        values.append(product_id)
        cursor.execute(query, tuple(values))
        connection.commit()

    cursor.close()
    connection.close()

# Function to delete a product
def delete_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    connection.commit()
    cursor.close()
    connection.close()

# Function to get low stock products
def get_low_stock_products(threshold=10):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, stock_quantity FROM products WHERE stock_quantity <= %s", (threshold,))
    low_stock_products = cursor.fetchall()
    cursor.close()
    connection.close()
    return [{'id': row[0], 'name': row[1], 'stock_quantity': row[2]} for row in low_stock_products]
