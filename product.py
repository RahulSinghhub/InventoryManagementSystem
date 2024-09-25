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
    
    # Only execute if there are fields to update
    if update_fields:
        query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
        values.append(product_id)
        cursor.execute(query, tuple(values))
        connection.commit()

    cursor.close()
    connection.close()
