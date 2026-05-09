import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_pass = os.getenv("DB_PASSWORD")

def get_connection():
    try:
        con = psycopg2.connect(user="postgres", 
                               password = db_pass,
                               host = "127.0.0.1",
                               port = "5432",
                               database = "Health_monitor")
        return con

    except Exception as e:
        print(f"Error while connecting to PostgreSQL: {e}")