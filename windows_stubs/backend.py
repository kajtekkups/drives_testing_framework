from common.opcua_communication import OpcuaCommunication
from backend.system_engine import SystemEngine
from backend.data_logger import DataLogger, CSVStorage
from backend.motor_controller import MotorController
from windows_stubs.sensor_reader import TempReader

import numpy as np
from enum import Enum
import time

DATA_FILES_PATH = "./data/"  

# url = "opc.tcp://127.0.0.1"
# opcua_client = OpcuaCommunication(url)

csv_storage = CSVStorage(DATA_FILES_PATH)
data_logger = DataLogger(csv_storage) #, mqtt_publisher)

motor_controller = MotorController()
temp_reader = TempReader()
backend_engine = SystemEngine(data_logger, motor_controller, temp_reader)