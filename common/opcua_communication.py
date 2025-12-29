from opcua import Client
from opcua import ua
from common.data_classes import Connectionstatus
import common.drive_parameters as param

from opcua.ua.uaerrors import UaStatusCodeError
import socket

#TODO: make sure opcua client reconects each time the connection is lost during program runtime
OPCUA_TIMEOUT = 1

class OpcuaCommunication:
    def __init__(self, url):
        self.url = url
        self.client = Client(url, OPCUA_TIMEOUT)
        self.root = None
        self.initial_connection = False
        self.connected = False

    def get_connection_status(self) -> Connectionstatus:
        if self.initial_connection:
            _ = self.read_parameter(param.MOTOR_TORQUE) # workaround, opcua doesn't have connection status method, we need to implement it ourself
        return Connectionstatus(self.url, self.connected) #TODO: make it work


    def write_parameter_float(self, setpoint, node_id):
        node = self.client.get_node(node_id)    
        node.set_value(ua.Variant(float(setpoint), ua.VariantType.Float)) 

    def read_parameter(self, node_id):
        try:
            node = self.client.get_node(node_id)
            value = node.get_value()
            self.connected = True
            return value
        except(UaStatusCodeError, socket.error, OSError) as e:
            self.connected = False
            print("read_parameter failed for %s: %s", node_id, e)
            return None

    def connect(self):
        while self.initial_connection == False:
            try:
                self.client.connect()
                print("Connected to server")
                self.connected = True
                self.initial_connection = True

                # Start from Root
                # self.root = self.client.get_root_node()
                # self.browse_nodes_children(self.root)
            except Exception as e:
                print(f"Could not connect to {self.url}: {e}")
    



class OpcuaCommunicationStub:
    def __init__(self, url):
        self.url = url
        self.client = Client(url)
        self.root = None
        self.connected = False
        self.initial_connection = False
    
    def get_connection_status(self) -> Connectionstatus:
        return Connectionstatus(self.url, self.connected)

    def write_parameter_float(self, setpoint, node_id):
        pass

    def read_parameter(self, node_id):
        return 0

    def connect(self):
        print("Connected to server")    
        self.connected = True
        self.initial_connection = True