import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager
load_dotenv()

db_pass = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("HOST")
db_port = os.getenv("PORT")

@contextmanager
def get_connection():
    con = None
    try:
        con = psycopg2.connect(user="postgres", 
                               password = db_pass,
                               host = db_host,
                               port = db_port,
                               database = db_name)
        yield con
        con.commit()
    except Exception as e:
        if con:
            con.rollback()
        raise e
    finally:
        if con:
            con.close()

    