# 1. Connect with drives
# 2. log data from drives
# 3. trigger motors, set torque/speed
# 4. set specified test map
from enum import Enum, auto
import numpy as np

class MotorState(Enum):
    IDLE = auto()
    RUNNING = auto()
    ERROR = auto()


class MotorController:
    def __init__(self):
        self._state = MotorState.IDLE
        self._velocity_setpoint = 0 

# --- Public API ---
    # @property
    def get_state(self):
        return self._state

    def test_drives_connection(self):
        pass
    
    def get_torque(self):
        pass

    def set_speed(self, velocity):
        #TODO: add mutex to prevent _
        #TODO: add ramp so the change of a setpoint isn't too big
        self._velocity_setpoint = velocity
      
    def get_speed(self):
        return self._velocity_setpoint #np.random.randint(1, 100)

    def run_motor_map(self):
        # this function will execute predefined motor map
        self._state = MotorState.RUNNING
    
    def running(self):
        return self._state == MotorState.RUNNING
    
    def reset(self):
        self.disable_motors()
        #TODO: more functionality

    def disable_motors(self):
        self._state = MotorState.IDLE

# --- Internal logic ---
    def _send_command(self, command):
        pass

    def _init_connection(self):
        pass