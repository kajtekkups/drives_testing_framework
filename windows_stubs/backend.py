from common.opcua_communication import OpcuaCommunication
from backend.system_engine import SystemEngine
from backend.data_logger import DataLogger, CSVStorage
from backend.motor_controller import MotorController
from windows_stubs.sensor_reader import TempReader

import numpy as np
from enum import Enum
import time

DATA_FILES_PATH = "./data/"  
OPCUA_URL = 'opc.tcp://localhost:4840'

opcua_client = OpcuaCommunication(OPCUA_URL)

csv_storage = CSVStorage(DATA_FILES_PATH)
data_logger = DataLogger(csv_storage) #, mqtt_publisher)

motor_controller = MotorController(opcua_client)
temp_reader = TempReader()
backend_engine = SystemEngine(data_logger, motor_controller, temp_reader)