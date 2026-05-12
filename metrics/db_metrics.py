from database.db import get_connection
from psycopg2.extras import RealDictCursor
import time

def get_con_metrics(samples = 5):
    totalcon_samples = []
    slowq_samples = []
    latency_samples = []
    maxduration_samples = []
    maxreads_samples = []
    maxwrites_samples = []
    for _ in range(samples):
        with get_connection() as con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                start_time = time.perf_counter()
                cur.execute("SELECT 1;")
                cur.fetchone()
                end_time = time.perf_counter()
                latency = end_time - start_time
                
                cur.execute("""SELECT
                                count(*) AS total,
                                count(*) FILTER (WHERE state = 'active') AS active,
                                count(*) FILTER (WHERE state = 'idle') AS idle,
                                count(*) FILTER (WHERE state = 'active' AND (now() - query_start) > interval '2 seconds') AS slow_count,
                                EXTRACT(EPOCH FROM MAX(now() - query_start) FILTER (WHERE state = 'active')) AS max_duration,
                                EXTRACT(EPOCH FROM MAX(now() - query_start) FILTER (WHERE state = 'active' AND query ~* '^\s*SELECT')) AS max_read_duration,
                                EXTRACT(EPOCH FROM MAX(now() - query_start) FILTER (WHERE state = 'active' AND query ~* '^\s*(INSERT|UPDATE|DELETE)')) AS max_write_duration
                                FROM pg_stat_activity""")
                stats = cur.fetchone()
                if stats:
                    totalcon_samples.append(stats["total"])
                    slowq_samples.append(stats["slow_count"])
                    latency_samples.append(latency)
                    maxduration_samples.append(stats["max_duration"])
                    if(stats["max_read_duration"] is None):
                        maxreads_samples.append(0)
                    else:
                        maxreads_samples.append(stats["max_read_duration"])
                    
                    if(stats["max_write_duration"] is None):
                        maxwrites_samples.append(0)
                    else:
                        maxwrites_samples.append(stats["max_write_duration"])
                time.sleep(0.2)

    if not totalcon_samples:
        return {"total": 0, "active": 0, "idle": 0}
    return {
        "average_connections": int(sum(totalcon_samples)/len(totalcon_samples)),
        "slow_queries": int(sum(slowq_samples)/len(slowq_samples)),
        "db_latency": round(sum(latency_samples)/len(latency_samples),2),
        "longest_query": round(float(max(maxduration_samples)),2),
        "longest_read": round(float(max(maxreads_samples)),2),
        "longest_write": round(float(max(maxwrites_samples)),2)
    }
    
def get_db_size():
    with get_connection() as con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT pg_size_pretty(pg_database_size('Health_monitor')) AS size;")
                result = cur.fetchone()
                return result['size']
    return "N/A"