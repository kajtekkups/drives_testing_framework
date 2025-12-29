#TODO: add sensor check during class initialization (maybe during meassuring too?)

import librtd
from typing import Dict, Tuple
import time
from enum import Enum

class SensorID(Enum):
    SENSOR_1 = 1
    SENSOR_2 = 2
    SENSOR_3 = 3
    SENSOR_4 = 4
    SENSOR_5 = 5
    SENSOR_6 = 6
    SENSOR_7 = 7
    # SENSOR_8 = 8

class TempReader:
    def __init__(self) -> None:
        self._sensors = {sensor: 0.0 for sensor in SensorID}
        self._board_id = 0 # As stated in documentation

    def read_all(self) -> Tuple[Dict[SensorID, float], float]:
        for sensor in self._sensors:
            self._sensors[sensor] = self._read_sensor(sensor.value)
        return self._sensors, time.time()
        
    def _read_sensor(self, sensor: int) -> float:                       
        return librtd.get(self._board_id, sensor)