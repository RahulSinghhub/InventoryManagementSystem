import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='exl_project',
        user='root',
        password='1234'
    )
