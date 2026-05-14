from db import get_connection

def init_tables():
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS objects(
            id SERIAL PRIMARY KEY,
            name TEXT,
            quantity INTEGER
        )
        """) # Create mock tables to operate on within our simulation
            
if __name__ == "__main__":
    init_tables()