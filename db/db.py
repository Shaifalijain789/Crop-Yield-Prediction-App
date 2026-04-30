import mysql.connector
from mysql.connector import Error

def get_connection(database=None):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database=database
        )
        if connection.is_connected():
            print("Connection established successfully!")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
