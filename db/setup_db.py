from db import get_connection
from mysql.connector import Error

def setup_signup_database():
    connection = None
    cursor = None
    try:
        # Step 1: connect without database first
        connection = get_connection()
        if connection is None:
            return
        
        cursor = connection.cursor()

        # Step 2: Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS Crop_Yield_Prediction")
        print("Database 'Crop_Yield_Prediction' created.")

        # Step 3: Switch to the database
        cursor.execute("USE Crop_Yield_Prediction")

        # Step 4: Create users table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print("Table 'users' created or already exists.")

    except Error as e:
        print(f"Database setup error: {e}")
    finally:
        
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("Connection closed.")

# Run setup
if __name__ == "__main__":
    setup_signup_database()
