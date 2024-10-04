import tkinter as tk
from tkinter import messagebox
from sales import generate_sales_report

def show_report_menu():
    # Create a new window for viewing sales reports
    report_menu = tk.Toplevel()
    report_menu.title("Sales Report")
    report_menu.geometry("400x200")
    report_menu.configure(bg="#2c3e50")

    # Set fonts and colors
    label_font = ("Helvetica", 16, "bold")
    button_font = ("Helvetica", 12, "bold")
    instruction_font = ("Helvetica", 12, "bold")
    label_color = "#ffffff"

    # Sales report label
    report_label = tk.Label(report_menu, text="Sales Report", font=label_font, bg="#2c3e50", fg=label_color)
    report_label.pack(pady=20)

    # Instruction label with improved styling
    instruction_label = tk.Label(
        report_menu,
        text="View top 5 products by sales:",
        font=instruction_font,
        bg="#2c3e50",
        fg=label_color,
        pady=10
    )
    instruction_label.pack()

    # Show report button
    def handle_show_report():
        generate_sales_report()
        report_menu.destroy()

    # Styled "Show Sales Report" button
    show_report_button = tk.Button(
        report_menu, 
        text="Show Sales Report", 
        font=button_font, 
        bg="#27ae60", 
        fg="#ffffff", 
        bd=0, 
        width=20, 
        height=2, 
        command=handle_show_report
    )
    show_report_button.pack(pady=20)

    report_menu.mainloop()
