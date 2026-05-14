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
# User specific data from the env

def init():
    con = None # We initialise it as None so that it is defined in the "finally" block
    try:
        con = psycopg2.connect(user="postgres", 
                               password = db_pass,
                               host = db_host,
                               port = db_port,
                               dbname = "postgres") # values will be drawn from .env
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Databases cannot be created while in a transanction, so we set it to autocommit
        with con.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,)) # Check if database exists
            if not cur.fetchone():
                query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                cur.execute(query)
                print("Database created") # If database doesnt exist, we create it, notice how only the init method can create it
            else:
                print("Database already exists")
    except Exception as e:
        print(str(e))
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    init()