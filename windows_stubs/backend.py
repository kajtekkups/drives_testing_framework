from common.opcua_communication import OpcuaCommunication
import numpy as np
from enum import Enum
import time

class SensorID(Enum):
    SENSOR_1 = 1
    SENSOR_2 = 2
    SENSOR_3 = 3
    SENSOR_4 = 4
    SENSOR_5 = 5
    SENSOR_6 = 6
    SENSOR_7 = 7
    # SENSOR_8 = 8

class SystemEngineStub:
    def __init__(self, opcua_client):
        self.time = 0
        self.counter = 0
        self.last_20_meassurements = {sensor: 0 for sensor in SensorID}
        self.opcua_client = opcua_client

    def run_test_loop(self):
        while True:
            self.run_test() 
            time.sleep(1)  

    def run_test(self):
        for key in self.last_20_meassurements:              
            self.last_20_meassurements[key] = np.random.randint(1, 100)

        self.time = self.counter
        self.counter += 1
    
    def test_running(self):
        return True
    
    def get_time(self):
        return self.time

    def get_measurements(self):
        return self.last_20_meassurements.copy()
    
url = "opc.tcp://127.0.0.1"
opcua_client = OpcuaCommunication(url)
backend_engine = SystemEngineStub(opcua_client)