from flask import jsonify, Blueprint
from tests.simulate_traffic import command_queue
simulate_bp = Blueprint('simulate', __name__)

@simulate_bp.route('/api/simulation/start', methods=['POST'])
def start_trigger():
    command_queue.put("START")
    return jsonify({"msg": "Command sent to manager"})

@simulate_bp.route('/api/simulation/stop', methods=['POST'])
def stop_trigger():
    command_queue.put("STOP")
    return jsonify({"msg": "Command sent to manager"})