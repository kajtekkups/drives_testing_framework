from test_runner import TestRunner
from data_logger import DataLogger, CSVStorage
# from mqtt_publisher import MqttPublisher
from motor_controller import MotorController
from sensor_reader import TempReader

DATA_FILES_PATH = "RTD/data/"  

# mqtt_publisher = MqttPublisher()
csv_storage = CSVStorage(DATA_FILES_PATH)
data_logger = DataLogger(csv_storage) #, mqtt_publisher)

motor_controller = MotorController()
temp_reader = TempReader()

test_runner = TestRunner(data_logger, motor_controller, temp_reader)

all_measurements=[]