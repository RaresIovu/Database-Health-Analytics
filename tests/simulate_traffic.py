from tests.simulation_service import get_all_knowledge, add_knowledge
import time
import threading
import queue

command_queue = queue.Queue() # Commands are sent to the queue through api calls, which are interpreted by the manager
active_worker = None

def simulation_manager():
    global active_worker
    stop_event = threading.Event() 
    while True: # Continuously listen for queue input
        try:
            command = command_queue.get(timeout=1) # Ensures that the thread does not block itself while listening for a new queue input
            
            if command == "START":
                if active_worker is None or not active_worker.is_alive(): # Ensures we only have 1 worker active at a time
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
    return active_worker is not None and active_worker.is_alive() # Effectively returns a bool on whether theres a mock client connected

def run_simulation(period, stop_event):
    while not stop_event.is_set():
        get_all_knowledge()
        add_knowledge("test_object", 100)
        time.sleep(period)
        # Mock client, simulates database queries that are collected by metric collector