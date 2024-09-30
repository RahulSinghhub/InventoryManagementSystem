import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import mysql.connector
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
from database import get_db_connection

# Function to train the model
def train_model():
    df = pd.read_csv('ml/draft_data.csv')

    # Preprocess the data
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Sort by Date to create lag features
    df = df.sort_values(by=['Product ID', 'Date'])

    # Create lag features (previous day and previous week sales)
    df['Sales_Lag_1'] = df.groupby('Product ID')['Sales'].shift(1)
    df['Sales_Lag_7'] = df.groupby('Product ID')['Sales'].shift(7)

    df.fillna(0, inplace=True)

    # Define features and target variable
    X = df[['Product ID', 'Unit Price', 'Year', 'Month', 'Day', 'Sales_Lag_1', 'Sales_Lag_7']]
    Y = df['Sales']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'trained_model.pkl')

    return model

# Function to fetch the last 7 days of sales data for a product
def get_sales_data(cursor, product_id):
    cursor.execute("""
        SELECT Sales FROM sales 
        WHERE product_id = %s 
        ORDER BY date DESC LIMIT 7
    """, (product_id,))
    return cursor.fetchall()

# Function to predict stock depletion using the trained model
# Function to predict stock depletion using the trained model
def predict_stock_depletion(product_id, stock_quantity, sales_data, model, unit_price, year, month, day):
    # Ensure that all features are of type float
    stock_quantity = float(stock_quantity)
    unit_price = float(unit_price)
    year = float(year)
    month = float(month)
    day = float(day)

    # Assuming sales_data is a list of quantities for the last 7 days
    sales_quantities = [float(sale[3]) for sale in sales_data]  # Assuming the 4th item in sales_data is the quantity

    # Creating the feature vector for prediction
    features = [product_id,stock_quantity, unit_price, year, month, day] + sales_quantities

    # Make sure the number of features matches what the model expects
    if len(features) == 7:  # Update this to the correct feature length your model expects
        days_remaining = model.predict([features])[0]
        return days_remaining
    else:
        raise ValueError(f"Expected 7 features, but got {len(features)}")




# Function to predict stock depletion for all products
def predict_restock_for_all_products():
    model = joblib.load('trained_model.pkl')

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT p.id, p.name, p.stock_quantity, p.unit_price, SUM(s.quantity) as total_sold
        FROM products p
        LEFT JOIN sales s ON p.id = s.product_id
        GROUP BY p.id
    """)

    results = cursor.fetchall()

    for row in results:
        product_id = row[0]
        product_name = row[1]
        stock_quantity = row[2]
        unit_price = row[3]

        # Fetch sales data for the product
        sales_data = get_sales_data(cursor, product_id)

        if sales_data:
            # Predict stock depletion
            predicted_days = predict_stock_depletion(product_id, stock_quantity, sales_data, model)
            print(f"Product {product_name} is predicted to run out of stock in {predicted_days:.2f} days.")

    cursor.close()
    connection.close()

# Function to check low stock and notify
def check_and_notify_low_stock():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, stock_quantity FROM products WHERE stock_quantity < 10")
    low_stock_products = cursor.fetchall()

    model = joblib.load('trained_model.pkl')

    for product in low_stock_products:
        product_id, name, stock_quantity = product

        # Fetch sales data for the product
        sales_data = get_sales_data(cursor, product_id)

        if sales_data:
            # Predict days remaining until stock depletion
            days_remaining = predict_stock_depletion(product_id, stock_quantity, sales_data, model)

            # Notify if stock will deplete in less than 5 days
            if days_remaining < 5:
                message = f'Stock for {name} is running out. Only {stock_quantity} left, will last {days_remaining:.2f} days.'
                print(message)  # You can replace this with an email notification or an alert in the UI

    cursor.close()
    connection.close()

# Function to run stock check continuously
def run_stock_check():
    while True:
        check_and_notify_low_stock()
        time.sleep(60 * 60)  # Check every hour

# Train the model before running stock checks
if __name__ == "__main__":
    train_model()
    predict_restock_for_all_products()
