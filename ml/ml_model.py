import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime, timedelta

from database import get_db_connection


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime, timedelta

# Load and preprocess the data
def train_model():
    # Step 1: Load the CSV into a DataFrame (for training)
    df = pd.read_csv("C:\\Users\\Jayant\\Desktop\\New folder\\draft_data.csv")

    # Step 2: Preprocess the data
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Sort by Date to create lag features
    df = df.sort_values(by=['Product ID', 'Date'])

    # Create lag features (previous day sales and previous week sales)
    df['Sales_Lag_1'] = df.groupby('Product ID')['Sales'].shift(1)  # Previous day sales
    df['Sales_Lag_7'] = df.groupby('Product ID')['Sales'].shift(7)  # Previous week sales

    # Fill missing lag values with 0
    df.fillna(0, inplace=True)

    # Define features (X) and target variable (Y)
    X = df[['Product ID', 'Unit Price', 'Year', 'Month', 'Day', 'Sales_Lag_1', 'Sales_Lag_7']]
    Y = df['Sales']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Create a Linear Regression model
    model = LinearRegression()

    # Train the model using the training data
    model.fit(X_train, y_train)

    # Return the trained model
    return model

# Function to predict when stock will run out for a single product
def predict_restock(product_id, stock_quantity, sales_data, model):
    # Calculate 1-day and 7-day lag values
    sales_lag_1 = sales_data[0][0]  # Latest sales (1-day lag)
    sales_lag_7_values = [entry[0] for entry in sales_data]  # List of the last 7 days of sales

    restock_threshold = 100  # Adjust this threshold as needed
    days_until_restock = 0
    today = datetime.today()  # This will be updated with each iteration
    unit_price = 20  # Assuming a constant unit price, adjust if needed

    # Loop to predict daily sales and calculate how long the stock will last
    while stock_quantity > restock_threshold:
        # Prepare features for prediction
        year = today.year
        month = today.month
        day = today.day

        # Predict sales for the next day
        features = np.array([[product_id, unit_price, year, month, day, sales_lag_1, sales_lag_7_values[0]]])
        predicted_sales_next_day = model.predict(features)[0]

        # Decrease the stock by the predicted daily sales
        stock_quantity -= predicted_sales_next_day
        days_until_restock += 1

        # Move to the next day
        today = today + timedelta(days=1)

        # Update lag features for the next day
        sales_lag_1 = predicted_sales_next_day  # The previous day's prediction becomes the next day's lag

        # Dynamically update sales_lag_7 by shifting the list and adding the new lag value
        if len(sales_lag_7_values) >= 7:
            sales_lag_7_values = [sales_lag_1] + sales_lag_7_values[:-1]  # Shift the values for the 7-day lag

    # Return the number of days until the stock runs out
    return days_until_restock, today.strftime('%Y-%m-%d')

# Function to predict restock for all products
def predict_restock_for_all_products(model):
    connection = get_db_connection()  # Assume this gets the existing database connection
    cursor = connection.cursor()

    # Fetch all product IDs and stock quantities from the products table
    cursor.execute("SELECT id, name, stock_quantity FROM products")
    products = cursor.fetchall()

    restock_predictions = []

    for product in products:
        product_id, name, stock_quantity = product

        # Fetch recent sales data for lag values (from 'sales' table)
        cursor.execute("""
            SELECT quantity FROM sales 
            WHERE product_id = %s 
            ORDER BY sale_date DESC LIMIT 7
        """, (product_id,))
        sales_data = cursor.fetchall()

        if sales_data:
            # Predict restock date for the product
            days_until_restock, restock_date = predict_restock(product_id, stock_quantity, sales_data, model)
            restock_predictions.append((product_id,name, days_until_restock, restock_date))

    cursor.close()
    connection.close()

    # Return the list of predictions for all products
    return restock_predictions

# Example function to call from frontend
def get_restock_status_for_all_products():
    # Load the trained model
    model = train_model()

    # Get restock status for all products
    restock_predictions = predict_restock_for_all_products(model)

    # Display or return the restock predictions
    if restock_predictions:
        return restock_predictions
    else:
        print("No products found or sales data missing.")




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
