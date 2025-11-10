import librtd
import time

from motor_controller import MotorState

class TestRunner:
    def __init__(self, data_logger, motor_controller, sensor_reader):
        self.data_logger = data_logger
        self.motor_controller = motor_controller
        self.sensor_reader = sensor_reader

    def monitor_meassurements(self, meassurements):
        # TODO: if temp is not in proper range, disable testing
        # TODO: if torque is not in proper range, disable testing?
        # TODO: if motor_speed is not in proper range, disable testing?

        # TODO: other dangerous cases?
        pass

    def run_test(self):
        self.motor_controller.trigger_motors()
        
        while self.motor_controller.get_state == MotorState.RUNNING:
            meassurements = self.sensor_reader.read_all()
            self.data_logger.log(meassurements)
            
            if self.monitor_meassurements(meassurements):
                self.motor_controller.disable_motors()
                #TODO: disable testing
                break
        
        self.motor_controller.disable_motors()