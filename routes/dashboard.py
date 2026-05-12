import json
from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/clear-logs', methods=['POST'])
def clear_logs():
    try:
        print("DELETED")
        with open('db_log.json', 'w') as f:
            json.dump([], f)
        return {"status": "success", "message": "Logs cleared"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500