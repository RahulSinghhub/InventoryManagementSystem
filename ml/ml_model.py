import pandas as pd
import numpy as np
from sklearn.externals import joblib
import mysql.connector
from datetime import datetime, timedelta
from ..task import email_tasks.send_email_notification
from database import get_db_connection


# Load pre-trained modelclear
model = joblib.load('ml/prediction.ipynb')

# Function to predict when stock will run out
def predict_stock_depletion(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch product data
    cursor.execute("SELECT stock_quantity, daily_sales FROM products WHERE id = %s", (product_id,))
    product_data = cursor.fetchone()

    if product_data:
        stock_quantity, daily_sales = product_data

        # Use the ML model to predict future sales
        features = np.array([[daily_sales]])  # Assuming daily sales is the feature for prediction
        predicted_sales_next_day = model.predict(features)[0]

        # Calculate how long the stock will last
        days_remaining = stock_quantity / predicted_sales_next_day

        cursor.close()
        connection.close()

        return days_remaining
    else:
        cursor.close()
        connection.close()
        return None

# Function to check stock and notify if running low
def check_and_notify_low_stock():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch products with low stock threshold
    cursor.execute("SELECT id, name, stock_quantity FROM products WHERE stock_quantity < 10")
    low_stock_products = cursor.fetchall()

    for product in low_stock_products:
        product_id, name, stock_quantity = product

        # Predict how many days the stock will last
        days_remaining = predict_stock_depletion(product_id)

        # Send notification 5 days prior to depletion
        if days_remaining and days_remaining < 5:
            message = f"Stock for {name} is running out. Only {stock_quantity} left. Estimated to last {days_remaining:.2f} days."
            send_email_notification(message)  # Send email
            print(message)  # Notify via interface (this would show in the interface)
    
    cursor.close()
    connection.close()

# Function to run real-time stock checks
def run_stock_check():
    while True:
        check_and_notify_low_stock()
        time.sleep(60 * 60)  # Check every hour (or adjust this interval)
