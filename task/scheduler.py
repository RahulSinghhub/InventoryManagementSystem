import schedule
import time
from stock_check import check_and_notify_low_stock

# Scheduler to run the task every hour
schedule.every().hour.do(check_and_notify_low_stock)

# Function to run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait for 1 minute before checking again
