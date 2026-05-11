import time
from json_service import save_to_json
from metrics.db_metrics import get_con_metrics, get_db_size
from metrics.system_metrics import get_sys_metrics

def collect_metrics():
    while True:
        metrics = {
            "connections": get_con_metrics(),
            "system": get_sys_metrics(),
            "db_size": get_db_size()
        }
        save_to_json(metrics)
        time.sleep(60)
    
