from opcua import Client
from opcua import ua

#TODO: make sure opcua client reconects each time the connection is lost during program runtime

class OpcuaCommunication:
    def __init__(self, url):
        self.url = url
        self.client = Client(url)
        self.root = None
        self.connected = False

    def write_parameter_float(self, setpoint, node_id):
        node = self.client.get_node(node_id)    
        node.set_value(ua.Variant(float(setpoint), ua.VariantType.Float)) 

    def read_parameter(self, node_id):
        node = self.client.get_node(node_id)
        return node.get_value()

    def connect(self):
        while self.connected == False:
            try:
                self.client.connect()
                print("Connected to server")
                self.connected = True

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

    def write_parameter_float(self, setpoint, node_id):
        pass

    def read_parameter(self, node_id):
        return 0

    def connect(self):
        print("Connected to server")    
        self.connected = True