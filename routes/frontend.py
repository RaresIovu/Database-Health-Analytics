from flask import Blueprint, render_template, jsonify
from json_service import get_all_logs
from tests.simulate_traffic import get_sim_state

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/dashboard')
def dashboard():
    try:
        all_metrics = get_all_logs(filename="db_log.json")
        all_ai_logs = get_all_logs(filename="ai_insights.json")
        return render_template('dashboard.html', metrics = all_metrics, ai_logs = all_ai_logs, is_running = get_sim_state())
        # We pass the metrics and AI insights to show in the dashboard, the run state of the simulation is passed for the sim buttons
    except Exception as e:
        return jsonify({"error": str(e)})
    
@frontend_bp.route('/detailedreport')
def detailed_report():
    try:
        all_logs = get_all_logs(filename="db_log.json")
        return render_template('detailedreport.html', metrics = all_logs) # We only need the metrics here
    except Exception as e:
        return jsonify({"error": str(e)})
    
@frontend_bp.route('/aireports')
def ai_logs():
    try:
        all_logs = get_all_logs(filename="ai_insights.json") # And only the AI insights here
        return render_template('ai_logs.html', insights = all_logs)
    except Exception as e:
        return jsonify({"error": str(e)})