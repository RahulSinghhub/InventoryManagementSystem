import joblib
from database import get_db_connection
from ml.ml_model import predict_stock_depletion
from task.email_tasks import send_email_notification


def check_and_notify_low_stock():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, stock_quantity, price FROM products WHERE stock_quantity < 150")
    low_stock_products = cursor.fetchall()

    model = joblib.load('trained_model.pkl')

    for product in low_stock_products:
        product_id, name, stock_quantity, unit_price = product

        cursor.execute("""
        SELECT YEAR(s.sale_date), MONTH(s.sale_date), DAY(s.sale_date), s.quantity
        FROM sales s
        WHERE s.product_id = %s
        ORDER BY s.sale_date DESC LIMIT 7
        """, (product_id,))

        sales_data = cursor.fetchall()

        if sales_data:
            # Extract year, month, day, and sales quantity
            year, month, day, quantity = sales_data[0]  # Assuming the most recent sale date
            days_remaining = predict_stock_depletion(product_id, stock_quantity, sales_data, model, unit_price, year, month, day)

            if days_remaining < 5:
                print(f"Stock for {name} is running out. Only {stock_quantity} left, will last {days_remaining:.2f} days.")
                send_email_notification(name, stock_quantity, days_remaining)

    cursor.close()
    connection.close()


def get_prediction_results():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, stock_quantity, price FROM products WHERE stock_quantity < 150")
    low_stock_products = cursor.fetchall()

    model = joblib.load('trained_model.pkl')
    prediction_results = []

    for product in low_stock_products:
        product_id, name, stock_quantity, unit_price = product

        cursor.execute("""
        SELECT YEAR(s.sale_date), MONTH(s.sale_date), DAY(s.sale_date), s.quantity
        FROM sales s
        WHERE s.product_id = %s
        ORDER BY s.sale_date DESC LIMIT 7
        """, (product_id,))

        sales_data = cursor.fetchall()

        if sales_data:
            # Extract year, month, day, and sales quantity
            year, month, day, quantity = sales_data[0]  # Assuming the most recent sale date
            days_remaining = predict_stock_depletion(product_id, stock_quantity, sales_data, model, unit_price, year, month, day)
            prediction_results.append((name, stock_quantity, days_remaining))

    cursor.close()
    connection.close()

    return prediction_results
