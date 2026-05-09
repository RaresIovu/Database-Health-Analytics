from database.db import get_connection
from psycopg2.extras import RealDictCursor
from system_metrics import print_sys_metrics
def get_connection_metrics():
    try:
        con = get_connection()
        if con is None:
            return {"total": 0, "active": 0, "idle": 0}
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT
                        count(*) AS total,
                        count(*) FILTER (WHERE state = 'active') AS active,
                        count(*) FILTER (WHERE state = 'idle') AS idle
                        FROM pg_stat_activity""")
        stats = cur.fetchone()
    except Exception as e:
        print(f"Error while providing the metrics: {e}")
    finally:
        con.close()
    return stats
    

def print_con_metrics():
    metrics = get_connection_metrics()
    print(f"Total connections: {metrics['total']}")
    print(f"Active: {metrics['active']}")
    print(f"Idle: {metrics['idle']}")


if(__name__ == "__main__"):
    print_con_metrics()
    print_sys_metrics()
    