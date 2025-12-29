# 1. Connect with drives
# 2. log data from drives
# 3. trigger motors, set torque/speed
# 4. set specified test map
from common.data_classes import Connectionstatus
from common.server import ServerInstance
import common.drive_parameters as param

from enum import Enum, auto
import bisect


class MotorState(Enum):
    IDLE = auto()
    RUNNING = auto()
    ERROR = auto()


class MotorController(ServerInstance):
    def __init__(self, client):
        self._state = MotorState.IDLE
        self._velocity_setpoint = 0 
        self.client = client



# --- Public API ---
    # @property
    def initialize(self):
        self.client.connect()

    def get_connection_status(self) -> Connectionstatus:
        return self.client.get_connection_status()
    
    def read_parameter(self, parameter_id):
        return self.client.read_parameter(parameter_id) 

    def get_state(self):
        return self._state

    def test_drives_connection(self):
        pass
    
    def get_torque(self):
        #TODO: add mock for testing without VD, np.random.randint(1, 100) 
        #TODO: should mutex be added?
        return self.client.read_parameter(param.MOTOR_TORQUE) 
    
    def get_stpoint(self):
        return self._velocity_setpoint
    
    def set_speed(self, velocity):
        #TODO: add mutex to prevent _
        #TODO: add ramp so the change of a setpoint isn't too big
        #TODO: should mutex be added?
        self._velocity_setpoint = velocity
        self.client.write_parameter_float(velocity, param.SET_SPEED_NODE_ID)
      
    def get_speed(self):
        #TODO: add mock for testing without VD, np.random.randint(1, 100) 
        #TODO: should mutex be added?
        #TODO: speed is predicted here, use parameter 1.1
        return self.client.read_parameter(param.ESTIMATED_SPEED_NODE_ID) 
    
    def bracket_index(self, current_time, timestamps):
        #TODO: refactor and test this function
        """
        Returns i such that timestamps[i] <= current_time < (timestamps[i+1]or test_time).
        Assumes timestamps is sorted ascending and has length >= 2.
        Returns:
        - i in [0, len(timestamps)-2] if bracket exists,
        - None if current_time is out of range (before first or after last).
        """
        if not timestamps or len(timestamps) < 2:
            return None

        # Find insertion point to keep list sorted
        pos = bisect.bisect_right(timestamps, current_time)

        # Now pos is the index where current_time would be inserted to the right
        # The bracket is (pos-1, pos)
        i = pos - 1

        # Validate that we are within bounds and the inequality holds
        if timestamps[i] <= current_time:
            return i
        return None

    def run_motor_map_speed(self, current_time, timestamp_points, rpm_points):
        self._state = MotorState.RUNNING

        rpm_index = self.bracket_index(current_time, timestamp_points)
        if rpm_index is None:
            self.disable_motors()
        elif rpm_index < len(rpm_points):
            self.set_speed(rpm_points[rpm_index])
        else:
            #TODO: handle error properly
            self.disable_motors()

    def run_motor_map_torque(self, current_time, timestamp_points, torque_points):
        pass

    def trigger_motor(self):
        self._state = MotorState.RUNNING

    def running(self):
        return self._state == MotorState.RUNNING
    
    def reset(self):
        self.disable_motors()
        #TODO: more functionality

    def disable_motors(self):
        self._state = MotorState.IDLE