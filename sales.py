from config import get_db_connection
import matplotlib.pyplot as plt

def generate_sales_report():
    # Establish database connection
    connection = get_db_connection()
    cursor = connection.cursor()

    # SQL query to get top 5 best-selling products in the last 7 days
    query = """
        SELECT p.name, SUM(s.quantity) as total_sales, p.stock_quantity
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE s.sale_date >= NOW() - INTERVAL 7 DAY
        GROUP BY p.id
        ORDER BY total_sales DESC
        LIMIT 5
    """
    cursor.execute(query)
    sales_data = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    if sales_data:
        # Extract product names, sales, and stock levels from the fetched data
        product_names = [row[0] for row in sales_data]
        total_sales = [row[1] for row in sales_data]
        stock_levels = [row[2] for row in sales_data]

        # Set up the plot design
        fig, ax = plt.subplots(figsize=(10, 6), facecolor="#f4f4f8")
        bars = ax.bar(product_names, total_sales, color="#34495e", alpha=0.85)

        # Add stock information above the bars
        for bar, stock in zip(bars, stock_levels):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, 
                    f'Stock: {stock}', ha='center', fontsize=10, color='#2c3e50')

        # Add gridlines for better readability
        ax.grid(True, which='both', axis='y', linestyle='--', color='#bdc3c7', alpha=0.6)

        # Customize plot appearance
        ax.set_facecolor("#ecf0f1")
        ax.set_title("Top 5 Best-Selling Products (Last Week)", fontsize=16, color="#2c3e50", pad=20)
        ax.set_xlabel("Product Names", fontsize=14, color="#2c3e50")
        ax.set_ylabel("Total Sales", fontsize=14, color="#2c3e50")

        # Set the color for axis ticks
        ax.tick_params(axis='x', colors='#2c3e50', labelsize=12)
        ax.tick_params(axis='y', colors='#2c3e50', labelsize=12)

        # Rotate product names for better readability
        plt.xticks(rotation=45, ha='right')

        # Finalize the layout
        plt.tight_layout()

        # Show the plot
        plt.show()
    else:
        print("No sales data available for the last 7 days.")
