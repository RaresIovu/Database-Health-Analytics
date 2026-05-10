from simulation_service import getAllKnowledge, addKnowledge
import time

def run_simulation(period):
    while True:
        getAllKnowledge()
        addKnowledge("test_object", 100)
        time.sleep(period)