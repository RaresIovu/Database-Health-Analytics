from service import get_all_logs
from flask import Flask, jsonify
import threading
from collector import collect_metrics

app = Flask(__name__, template_folder="templates")
@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        metrics = get_all_logs()
        return metrics
    except Exception as e:
        return jsonify({"eroare": "A survenit o eroare"})

if(__name__ == "__main__"):
    collector_thread = threading.Thread(target=collect_metrics, daemon=True)
    collector_thread.start()
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)