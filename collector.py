import time
from json_service import save_to_json
from metrics.db_metrics import get_con_metrics, get_db_size
from metrics.system_metrics import get_sys_metrics
from ai_handler import generate_answer

def collect_metrics():
    ai_buffer = []
    while True:
        metrics = {
            "connections": get_con_metrics(),
            "system": get_sys_metrics(),
            "db_size": get_db_size()
        }
        ai_buffer.append(metrics)
        save_to_json(metrics, filename="db_log.json")
        if len(ai_buffer) >= 10:
            ai_response = {
                "response": generate_answer(ai_buffer)
            }
            save_to_json(ai_response, filename="ai_insights.json")
            ai_buffer = []

        time.sleep(60)
    
