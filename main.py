from test_runner import TestRunner
from data_logger import DataLogger
from mqtt_publisher import MqttPublisher
from motor_controller import MotorController
from sensor_reader import SensorReader

if __name__ == "__main__":    

    mqtt_publisher = MqttPublisher()
    data_logger = DataLogger(DATA_FILES_PATH, mqtt_publisher)
    motor_controller = MotorController()
    sensor_reader = SensorReader()

    test_runner = TestRunner(data_logger, mqtt_publisher, motor_controller, sensor_reader)
    test_runner.run_test()