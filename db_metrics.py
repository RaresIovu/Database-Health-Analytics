from database.db import get_connection
from psycopg2.extras import RealDictCursor

def get_con_metrics():
   
    with get_connection() as con:
        if con is None:
            return {"total": 0, "active": 0, "idle": 0}
        with con.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""SELECT
                            count(*) AS total,
                            count(*) FILTER (WHERE state = 'active') AS active,
                            count(*) FILTER (WHERE state = 'idle') AS idle
                            FROM pg_stat_activity""")
            stats = cur.fetchone()
    
    return stats
    
def get_db_size():
    with get_connection() as con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT pg_size_pretty(pg_database_size('Health_monitor')) AS size;")
                result = cur.fetchone()
                return result['size']
    return "N/A"