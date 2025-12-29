from opcua import Client
from opcua import ua

class OpcuaCommunication:
    def __init__(self, url):
        self.url = url
        self.client = Client(url)
        self.root = None
        self.connected = False
        
    def browse_nodes_children(self, node):
        try:
            print(f"Parent: {node.get_browse_name()} ({node.nodeid})")
        except:
            print(f"<unreadable> ({node})")
            return
        # Browse children
        for child in node.get_children():
            print("BrowseName:", child.get_browse_name(), "| NodeId:", child.nodeid.to_string())
            

    def get_child(self, node, target_name):
        for child in node.get_children():                    
            if child.get_browse_name().Name == target_name:
                print("Found node:", child)
                return child
        return None

    def set_speed_setpoint(self):
        # path = ["0:Objects", "1:Parameters", "10:022 Speed reference selection"]#, "Parameters", "022 Speed reference selection"]
        # return self.root.get_child(path)
    

    # 10:026 Constant speed 
        # namespace = "10"
        # name = "026 Constant speed 1"
        speed_node_id = "ns=10;i=1703958"
        node = self.client.get_node(speed_node_id)
        
        setpoint = input("Enter speed setpoint: ")

        node.set_value(ua.Variant(float(setpoint), ua.VariantType.Float)) 
        print("speed set")

    def connect(self):
        while self.connected == False:
            try:
                self.client.connect()
                print("Connected to server")
                self.connected = True

                # Start from Root
                self.root = self.client.get_root_node()
                self.browse_nodes_children(self.root)
            except Exception as e:
                print(f"Could not connect to {self.url}: {e}")
    

if __name__ == '__main__':
    url = 'opc.tcp://localhost:4840'
    opcua_communication = OpcuaCommunication(url)
    opcua_communication.connect()

    target_node = opcua_communication.root

    while True:            
        name = input("Enter node name: ")
        if name == "0":
            target_node = opcua_communication.set_speed_setpoint()
        else:
            new_target_node = opcua_communication.get_child(target_node, name)
            if new_target_node is not None:
                target_node = new_target_node            
        opcua_communication.browse_nodes_children(target_node)
