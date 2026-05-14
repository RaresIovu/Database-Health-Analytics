import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager
load_dotenv()

db_pass = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("HOST")
db_port = os.getenv("PORT")

@contextmanager #The usual behaviour of a postgres connection in context manager is that it automatically completes transaction
# I redefined the behaviour so that it also automatically closes the connection 
def get_connection(): # This returns a generator of connection, not a connection. The context manager (with get_connection() as con:) defines its behaviour
    con = None
    try:
        con = psycopg2.connect(user="postgres", 
                               password = db_pass,
                               host = db_host,
                               port = db_port,
                               database = db_name)
        yield con # Connection is yielded to the "block" which uses it, pausing this method. Only after it goes out of scope does it unpause and continue with commits and close
        con.commit() # Only after the connection was used do we commit the transaction
    except Exception as e:
        if con:
            con.rollback() # Upon any exception, we cancel the transaction. The exception can happen even if connection is being used
        raise e
    finally:
        if con:
            con.close() # Finally, we close the connection, regardless of whether the transaction was successful or not

    