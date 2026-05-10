import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
load_dotenv()
db_pass = os.getenv("DB_PASSWORD")
def init():
    con = None
    try:
        con = psycopg2.connect(user="postgres", 
                               password = db_pass,
                               host = "127.0.0.1",
                               port = "5432",
                               dbname = "postgres")
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with con.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'health_monitor'")
            if cur.fetchone():
                print("Database already initialised")
            else:
                cur.execute('CREATE DATABASE "health_monitor"')
                print("Database created")
    except Exception as e:
        print(e)
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    init()