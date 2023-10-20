import os
import sys
import time
import mysql.connector

def wait_for_db():
    max_retries = 30
    delay_between_retries = 2  # seconds
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
            )
            connection.close()
            print("Database is ready. Continuing with Django startup.")
            return
        except mysql.connector.Error as err:
            print(f"Database connection attempt {attempt + 1}/{max_retries} failed: {err}")
            time.sleep(delay_between_retries)
    else:
        print("Unable to connect to the database after multiple attempts.")
        sys.exit(1)

if __name__ == "__main__":
    wait_for_db()

