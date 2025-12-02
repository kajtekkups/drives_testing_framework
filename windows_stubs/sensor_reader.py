import time
from enum import Enum
import numpy as np


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
    def __init__(self):
        self._sensors = {sensor: 0 for sensor in SensorID}
        self._board_id = 0 # As stated in documentation

    def read_all(self):
        for sensor in self._sensors:
            self._sensors[sensor] = np.random.randint(1, 100)
        return self._sensors, time.time()