from common.opcua_communication import OpcuaCommunication, OpcuaCommunicationStub
from common.data_classes import ServerId
from backend.system_engine import SystemEngine
from backend.data_logger import DataLogger, CSVStorage
# from mqtt_publisher import MqttPublisher
from backend.motor_controller import MotorController
from backend.sensor_reader import TempReader

DATA_FILES_PATH = "RTD/data/"  
# OPCUA_URL_DRIVE_1 = 'opc.tcp://localhost:4840'
OPCUA_URL_DRIVE_1 = 'opc.tcp://192.168.0.104:4840'
OPCUA_URL_DRIVE_2 = 'opc.tcp://localhost:4845'

# opcua_client_drive_1 = OpcuaCommunicationStub(OPCUA_URL_DRIVE_1)
opcua_client_drive_2 = OpcuaCommunicationStub(OPCUA_URL_DRIVE_2)

opcua_client_drive_1 = OpcuaCommunication(OPCUA_URL_DRIVE_1)
# opcua_client_drive_2 = OpcuaCommunication(OPCUA_URL_DRIVE_2)

# mqtt_publisher = MqttPublisher()
csv_storage = CSVStorage(DATA_FILES_PATH)
data_logger = DataLogger(csv_storage) #, mqtt_publisher)

motor_controller = MotorController(opcua_client_drive_1)
load_controller = MotorController(opcua_client_drive_2)
temp_reader = TempReader()

drive_connections = {
        ServerId.motor_drive: motor_controller,
        # ServerId.load_drive: None,
        ServerId.load_drive: load_controller,
        # ServerId.mqtt_1: None        
        }
backend_engine = SystemEngine(data_logger, temp_reader, drive_connections)