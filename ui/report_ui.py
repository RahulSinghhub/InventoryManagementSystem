import tkinter as tk
from tkinter import messagebox
from sales import generate_sales_report

def show_report_menu():
    # Create a new window for viewing sales reports
    report_menu = tk.Toplevel()
    report_menu.title("Sales Report")
    report_menu.geometry("300x100")

    tk.Label(report_menu, text="Click below to view the sales report").pack(pady=10)

    # Show report button
    def handle_show_report():
        generate_sales_report()
        report_menu.destroy()

    tk.Button(report_menu, text="Show Sales Report", command=handle_show_report).pack(pady=10)
