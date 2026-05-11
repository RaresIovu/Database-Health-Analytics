from tests.simulation_service import get_all_knowledge, add_knowledge
import time

def run_simulation(period):
    while True:
        get_all_knowledge()
        add_knowledge("test_object", 100)
        time.sleep(period)