import tkinter as tk
from stock_check import get_prediction_results

def show_predictions():
    # Create a new window for predictions
    prediction_window = tk.Toplevel()
    prediction_window.title("Stock Predictions")

    # Fetch predictions from stock_check.py
    predictions = get_prediction_results()

    # Add a label to show predictions
    prediction_label = tk.Label(prediction_window, text="Stock Predictions", font=("Helvetica", 14))
    prediction_label.pack(pady=10)

    # If predictions are empty, show a message
    if not predictions:
        empty_label = tk.Label(prediction_window, text="No predictions available", font=("Helvetica", 12))
        empty_label.pack(pady=10)
    else:
        # Add the prediction results to the window
        for prediction in predictions:
            product_name, stock_quantity, days_remaining = prediction
            result_text = f"Product: {product_name} | Stock: {stock_quantity} | Days remaining: {days_remaining}"
            result_label = tk.Label(prediction_window, text=result_text, font=("Helvetica", 12))
            result_label.pack(pady=5)

    # Add a close button
    close_button = tk.Button(prediction_window, text="Close", command=prediction_window.destroy)
    close_button.pack(pady=10)
