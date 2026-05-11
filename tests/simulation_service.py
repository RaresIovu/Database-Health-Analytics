from database.db import get_connection
import random
def get_all_knowledge():
    with get_connection() as con:
        with con.cursor() as cur:
            if random.random() < 0.05:
                cur.execute("SELECT pg_sleep(10);")
            cur.execute("SELECT id, name, quantity FROM objects")
        
def add_knowledge(name, quantity):
    with get_connection() as con:
        with con.cursor() as cur:
            if random.random() < 0.05:
                cur.execute("SELECT pg_sleep(10);")
            cur.execute("INSERT INTO objects (name, quantity) VALUES (%s, %s)", (name, quantity))