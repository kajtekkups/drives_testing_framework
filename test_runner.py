import librtd
import time

from MotorController import MotorState

DATA_FILES_PATH = "RTD/data/" #TODO: If not existing, create folder


class TestRunner:
    def __init__(self, data_logger, mqtt_publisher, motor_controller, sensor_reader):
        self.data_logger = data_logger
        self.motor_controller = motor_controller
        self.sensor_reader = sensor_reader

    def monitor_meassurements(self, temp, torque, motor_speed):
        # TODO: if temp is not in proper range, disable testing
        # TODO: if torque is not in proper range, disable testing?
        # TODO: if motor_speed is not in proper range, disable testing?

        # TODO: other dangerous cases?
        pass

    def run_test(self):
        self.motor_controller.trigger_motors()
        
        while self.motor_controller == MotorState.RUNNING:
            meassurements = self.sensor_reader.get_meassurements()
            self.data_logger.log_data(meassurements)
            
            if self.monitor_meassurements(meassurements['temp'], meassurements['torque'], meassurements['motor_speed']):
                # self.motor_controller.disable_motors()
                #TODO: disable testing
                break