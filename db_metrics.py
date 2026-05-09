from database.db import get_connection
from psycopg2.extras import RealDictCursor

def get_con_metrics():
    try:
        con = get_connection()
        if con is None:
            return {"total": 0, "active": 0, "idle": 0}
        with con.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""SELECT
                            count(*) AS total,
                            count(*) FILTER (WHERE state = 'active') AS active,
                            count(*) FILTER (WHERE state = 'idle') AS idle
                            FROM pg_stat_activity""")
            stats = cur.fetchone()
    except Exception as e:
        print(f"Error while providing the metrics: {e}")
    finally:
        if con:
            con.close()
    return stats
    
def get_db_size():
    con = get_connection()
    if con:
        try:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT pg_size_pretty(pg_database_size('Health_monitor')) AS size;")
                result = cur.fetchone()
                return result['size']
        finally:
            if con:
                con.close()
    return "N/A"

def print_con_metrics():
    metrics = get_con_metrics()
    print(f"Total connections: {metrics['total']}")
    print(f"Active: {metrics['active']}")
    print(f"Idle: {metrics['idle']}")

def print_db_size():
    print(get_db_size())