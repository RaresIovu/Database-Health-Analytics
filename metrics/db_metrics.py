from database.db import get_connection
from psycopg2.extras import RealDictCursor
import time

def get_con_metrics(samples = 5):
    totalcon_samples = []
    activecon_samples = []
    idlecon_samples = []
    for _ in range(samples):
        with get_connection() as con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""SELECT
                                count(*) AS total,
                                count(*) FILTER (WHERE state = 'active') AS active,
                                count(*) FILTER (WHERE state = 'idle') AS idle,
                                count(*) FILTER (WHERE state = 'active' AND (now() - query_start) > interval '2 seconds') AS slow_count,
                                EXTRACT(EPOCH FROM MAX(now() - query_start) FILTER (WHERE state = 'active')) AS max_duration
                                FROM pg_stat_activity""")
                stats = cur.fetchone()
                if stats:
                    totalcon_samples.append(stats["total"])
                    activecon_samples.append(stats["active"])
                    idlecon_samples.append(stats["idle"])
                time.sleep(0.2)

    if not totalcon_samples:
        return {"total": 0, "active": 0, "idle": 0}
    
    return {
        "average_connections": int(sum(totalcon_samples)/len(totalcon_samples)),
        "total_active": int(sum(activecon_samples)/len(activecon_samples)),
        "max_active": max(activecon_samples),
        "total_idle": int(sum(idlecon_samples)/len(idlecon_samples)),
        "slow_queries": stats["slow_count"],
        "longest_query": int(stats["max_duration"])
    }
    
def get_db_size():
    with get_connection() as con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT pg_size_pretty(pg_database_size('Health_monitor')) AS size;")
                result = cur.fetchone()
                return result['size']
    return "N/A"