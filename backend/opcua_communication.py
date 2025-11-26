from opcua import Client

class OpcuaCommunication:
    def __init__(self, url):
        self.url = url
        self.client = Client(url)

    def browse_nodes_recursive(self, node, level=0):
        indent = "  " * level
        try:
            print(f"{indent}- {node.get_browse_name()} ({node.nodeid})")
        except:
            print(f"{indent}- <unreadable> ({node.nodeid})")

        # Browse children
        for child in node.get_children():
            self.browse_nodes_recursive(child, level + 1)

    def connect(self):
        try:
            self.client.connect()
            print("Connected to server")

            # Start from Root
            root = self.client.get_root_node()

            self.browse_recursive(root)

        finally:
            print(f"\nCould not connect to {self.url}")