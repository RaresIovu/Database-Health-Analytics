from flask import Flask
import threading
from collector import collect_metrics
from tests.simulate_traffic import simulation_manager
from routes.dashboard import dashboard_bp
from routes.simulate import simulate_bp
from routes.frontend import frontend_bp

app = Flask(__name__, template_folder="templates")
app.register_blueprint(dashboard_bp)
app.register_blueprint(simulate_bp)
app.register_blueprint(frontend_bp)

if(__name__ == "__main__"):
    collector_thread = threading.Thread(target=collect_metrics, daemon=True)
    client_thread = threading.Thread(target=simulation_manager, daemon=True)
    collector_thread.start()
    client_thread.start()
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)