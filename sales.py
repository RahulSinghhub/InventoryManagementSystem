from config import get_db_connection
import matplotlib.pyplot as plt

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
