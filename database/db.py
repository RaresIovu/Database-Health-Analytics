import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager
load_dotenv()

db_pass = os.getenv("DB_PASSWORD")

@contextmanager
def get_connection():
    con = None
    try:
        con = psycopg2.connect(user="postgres", 
                               password = db_pass,
                               host = "127.0.0.1",
                               port = "5432",
                               database = "Health_monitor")
        yield con
        con.commit()
    except Exception as e:
        if con:
            con.rollback()
        raise e
    finally:
        if con:
            con.close()

    