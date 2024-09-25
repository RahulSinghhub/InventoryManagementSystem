from mysql.connector import Error
from config import get_db_connection

def setup_database():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Create the products table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                category VARCHAR(255),
                stock_quantity INT,
                price DECIMAL(10, 2)
            )
        """)
        
        # Create the sales table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT,
                quantity INT,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error while setting up the database: {e}")
