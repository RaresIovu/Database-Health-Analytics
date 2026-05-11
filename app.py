from json_service import get_all_logs
from flask import Flask, jsonify
import threading
from collector import collect_metrics
from tests.simulate_traffic import run_simulation

app = Flask(__name__, template_folder="templates")
@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        metrics = get_all_logs()
        return metrics
    except Exception as e:
        return jsonify({"eroare": str(e), "status": 500}), 500

if(__name__ == "__main__"):
    collector_thread = threading.Thread(target=collect_metrics, daemon=True)
    client_thread = threading.Thread(target=run_simulation, args=(0.1,), daemon=True)
    collector_thread.start()
    client_thread.start()
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)