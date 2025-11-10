# 1. Connect with drives
# 2. log data from drives
# 3. trigger motors, set torque/speed
# 4. set specified test map
from enum import Enum, auto

class MotorState(Enum):
    IDLE = auto()
    RUNNING = auto()
    ERROR = auto()