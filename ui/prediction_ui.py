import tkinter as tk
from ml.ml_model import get_restock_status_for_all_products

def show_predictions():
    # Create a new window for predictions
    prediction_window = tk.Toplevel()
    prediction_window.title("Stock Predictions")
    prediction_window.geometry("600x400")  # Adjust window size
    prediction_window.configure(bg="#ecf0f1")  # Light background

    # Fetch predictions from the model
    predictions = get_restock_status_for_all_products()

    # Add a label to show predictions title
    prediction_label = tk.Label(prediction_window, text="Stock Predictions", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ecf0f1", padx=10, pady=10)
    prediction_label.grid(row=0, column=0, columnspan=4, pady=(10, 20))

    # If predictions are empty, show a message
    if not predictions:
        empty_label = tk.Label(prediction_window, text="No predictions available", font=("Helvetica", 12), bg="#ecf0f1")
        empty_label.grid(row=1, column=0, columnspan=4, pady=10)
    else:
        # Add table headers
        headers = ["Product ID", "Name", "Days Remaining", "Restock Date"]
        header_bg = "#27ae60"  # Green background for headers
        cell_bg_even = "#ffffff"  # White background for even rows
        cell_bg_odd = "#f0f0f0"  # Light grey background for odd rows

        for col, header in enumerate(headers):
            header_label = tk.Label(prediction_window, text=header, font=("Helvetica", 12, "bold"), bg=header_bg, fg="#ffffff", padx=10, pady=5, relief=tk.RIDGE)
            header_label.grid(row=1, column=col, padx=5, pady=5, sticky="nsew")

        # Add the prediction results to the window in a structured way
        for row, prediction in enumerate(predictions, start=2):
            product_id, name, days_remaining, restock_date = prediction
            bg_color = cell_bg_even if row % 2 == 0 else cell_bg_odd

            tk.Label(prediction_window, text=product_id, font=("Helvetica", 12), bg=bg_color, padx=10, pady=5, relief=tk.SOLID).grid(row=row, column=0, padx=5, pady=5, sticky="nsew")
            tk.Label(prediction_window, text=name, font=("Helvetica", 12), bg=bg_color, padx=10, pady=5, relief=tk.SOLID).grid(row=row, column=1, padx=5, pady=5, sticky="nsew")
            tk.Label(prediction_window, text=days_remaining, font=("Helvetica", 12), bg=bg_color, padx=10, pady=5, relief=tk.SOLID).grid(row=row, column=2, padx=5, pady=5, sticky="nsew")
            tk.Label(prediction_window, text=restock_date, font=("Helvetica", 12), bg=bg_color, padx=10, pady=5, relief=tk.SOLID).grid(row=row, column=3, padx=5, pady=5, sticky="nsew")

    # Add a close button at the bottom
    close_button = tk.Button(prediction_window, text="Close", command=prediction_window.destroy, bg="#c0392b", fg="#ffffff", font=("Helvetica", 12), padx=10, pady=5)
    close_button.grid(row=row+1, column=0, columnspan=4, pady=20)

