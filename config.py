import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='exl_project',
        user='root',
        password='1234'
    )

EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
RECIPIENT_EMAIL = "store_manager_email@example.com"
