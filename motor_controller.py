# 1. Connect with drives
# 2. log data from drives
# 3. trigger motors, set torque/speed
# 4. set specified test map
from enum import Enum, auto

class MotorState(Enum):
    IDLE = auto()
    RUNNING = auto()
    ERROR = auto()


class MotorController:
    def __init__(self):
        self._state = MotorState.IDLE

# --- Public API ---
    @property
    def get_state(self):
        return self._state

    def test_drives_connection(self):
        pass
    
    def get_torque(self):
        pass

    def get_speed(self):
        pass

    def trigger_motors(self):
        self._state = MotorState.RUNNING

    def disable_motors(self):
        self._state = MotorState.IDLE

# --- Internal logic ---
    def _send_command(self, command):
        pass

    def _init_connection(self):
        pass