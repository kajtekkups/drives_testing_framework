#TODO: add sensor check during class initialization (maybe during meassuring too?)

import librtd
from typing import Dict, Tuple, List
import time
from enum import Enum
import copy

class SensorID(Enum):
    SENSOR_1 = 1
    SENSOR_2 = 2
    SENSOR_3 = 3
    SENSOR_4 = 4
    SENSOR_5 = 5
    SENSOR_6 = 6
    SENSOR_7 = 7
    SENSOR_8 = 8

MIN_CONNECTION_TRESHOLD = 0
MAX_CONNECTION_TRESHOLD = 100

class TempReader:
    def __init__(self) -> None:
        self._sensors = {sensor: 0.0 for sensor in SensorID}
        self._board_id = 0 # As stated in documentation

    def read_all(self) -> Tuple[Dict[SensorID, float], float]:
        for sensor in self._sensors:
            self._sensors[sensor] = self._read_sensor(sensor.value)
        return copy.deepcopy(self._sensors), time.time() #TODO: return a deep copy
    
    def get_sensors_status(self) -> Dict[str, bool]:
        status_list: Dict[str, bool] = {}
        for sensor in self._sensors:
            #TODO: there is no build in option for checking weather sensor is connected, this is workaround
            temp = self._read_sensor(sensor.value)
            if MIN_CONNECTION_TRESHOLD < temp < MAX_CONNECTION_TRESHOLD:
                connected = True
            else:
                connected = False

            status_list[f"Temp sensor {sensor}"] = connected
        
        return status_list

    def _read_sensor(self, sensor: int) -> float:                       
        return librtd.get(self._board_id, sensor)