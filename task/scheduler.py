import schedule
import time
from email_tasks import send_email_notification
from ml.ml_model import predict_sales

def check_stock_levels():
    # Logic to retrieve stock levels from the database
    stock_data = fetch_stock_data()
    
    # Prediction for future sales
    predicted_sales = predict_sales(stock_data)
    
    for product, days_left in predicted_sales.items():
        if days_left <= 5:  # If stock will last less than 5 days
            send_email_notification(
                subject=f"Low stock alert for {product}",
                body=f"Stock for {product} will finish in {days_left} days."
            )

# Schedule the task every day at 9 AM
schedule.every().day.at("09:00").do(check_stock_levels)

while True:
    schedule.run_pending()
    time.sleep(60)  # Wait one minute before checking again
