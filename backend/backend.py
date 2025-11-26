from backend.system_engine import SystemEngine
from backend.data_logger import DataLogger, CSVStorage
# from mqtt_publisher import MqttPublisher
from backend.motor_controller import MotorController
from backend.sensor_reader import TempReader

DATA_FILES_PATH = "RTD/data/"  

# mqtt_publisher = MqttPublisher()
csv_storage = CSVStorage(DATA_FILES_PATH)
data_logger = DataLogger(csv_storage) #, mqtt_publisher)

motor_controller = MotorController()
temp_reader = TempReader()

backend_engine = SystemEngine(data_logger, motor_controller, temp_reader)