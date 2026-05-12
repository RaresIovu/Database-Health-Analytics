from flask import Blueprint, render_template
from json_service import get_all_logs
from tests.simulate_traffic import get_sim_state

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/dashboard')
def dashboard():
    all_logs = get_all_logs()
    return render_template('dashboard.html', metrics = all_logs, is_running = get_sim_state())

@frontend_bp.route('/detailedreport')
def detailed_report():
    all_logs = get_all_logs()
    return render_template('detailedreport.html', metrics = all_logs)