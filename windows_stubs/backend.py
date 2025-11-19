import numpy as np
import time

class TestRunner:
    def __init__(self):
        self.meassurements = {"T1": 1,
                              "T2": 2,
                              "T3": 3,
                              "T4": 4,
                              "T5": 5,
                              "T6": 6,
                              "T7": 7,
                              "T8": 8,
                              "T9": 8,
                              "T10": 8}
        self.state = "RUNNING"
        self.time = []
        self.counter = 0
        self.last_20_meassurements = {
                              "T1": [],
                              "T2": [],
                              "T3": [],
                              "T4": [],
                              "T5": [],
                              "T6": [],
                              "T7": [],
                              "T8": [],
                              "T9": [],
                              "T10": []}
        
        self.MAX_DATA_LENGTH = 10
    
    def run_test_loop(self):
        while True:
            test_runner.run_test() 
            time.sleep(1)  

    def run_test(self):
        for key in self.last_20_meassurements:
            if len(self.last_20_meassurements[key]) == self.MAX_DATA_LENGTH:
                self.last_20_meassurements[key].pop(0)                
            self.last_20_meassurements[key].append(np.random.randint(1, 100))

        if len(self.time) == self.MAX_DATA_LENGTH:
            self.time.pop(0)
        self.time.append(self.counter)
        self.counter += 1
    
    def test_running(self):
        return True
    
    def get_time(self):
        return self.time.copy()

    def get_measurements(self):
        return self.last_20_meassurements.copy()
    
test_runner = TestRunner()
all_measurements=[]