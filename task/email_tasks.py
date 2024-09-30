import yagmail
from config import EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL

def send_email_notification(product_name, stock_quantity, days_remaining, recipient_email=RECIPIENT_EMAIL):
    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)

    subject = f"Low Stock Alert: {product_name}"
    body = f"""
    Dear Store Manager,

    The stock for {product_name} is running low. 
    Current Stock: {stock_quantity} units
    Expected to last: {days_remaining:.2f} days

    Please restock as soon as possible to avoid running out.

    Best regards,
    Inventory Management System
    """
    yag.send(to=recipient_email, subject=subject, contents=body)
    print(f"Email notification sent to {recipient_email} for product {product_name}.")

