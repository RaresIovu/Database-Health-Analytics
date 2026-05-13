from tests.simulation_service import get_all_knowledge, add_knowledge
import time
import threading
import queue

command_queue = queue.Queue()
active_worker = None

def simulation_manager():
    global active_worker
    stop_event = threading.Event() # A better way to signal threads to stop
    while True:
        try:
            # Check for a new command (non-blocking)
            command = command_queue.get(timeout=1)
            
            if command == "START":
                if active_worker is None or not active_worker.is_alive():
                    stop_event.clear()
                    active_worker = threading.Thread(
                        target=run_simulation, 
                        args=(0.5, stop_event), 
                        daemon=True
                    )
                    active_worker.start()
            elif command == "STOP":
                stop_event.set()
        except queue.Empty:
            continue

def get_sim_state():
    return active_worker is not None and active_worker.is_alive()

def run_simulation(period, stop_event):
    while not stop_event.is_set():
        get_all_knowledge()
        add_knowledge("test_object", 100)
        time.sleep(period)