from flask import jsonify, Blueprint
from json_service import get_all_logs

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def dashboard():
    try:
        metrics = get_all_logs()
        return metrics
    except Exception as e:
        return jsonify({"eroare": str(e), "status": 500}), 500