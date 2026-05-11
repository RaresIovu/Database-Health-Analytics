import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

db_pass = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("HOST")
db_port = os.getenv("PORT")

def init():
    con = None
    try:
        con = psycopg2.connect(user="postgres", 
                               password = db_pass,
                               host = db_host,
                               port = db_port,
                               dbname = "postgres")
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with con.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
            if not cur.fetchone():
                query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                cur.execute(query)
                print("Database created")
            else:
                print("Database already exists")
    except Exception as e:
        print(str(e))
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    init()