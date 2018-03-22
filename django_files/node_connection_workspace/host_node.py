"""
This class defines an object that represents a single parking lot host.
A host node will instantiate one instance of this per geographical lot it
manages (usually 1).

1. Send request to server for next available Lot ID
2. Create new Host object (give it unused name0 with this ID.
3. Pickle Host Object and Transmit to Server.

"""

from datetime import datetime

class PHost:
    """ Variables """
    host_id = None      # This value is provided by the server.
    host_name = None    # This string is given TO the server
    
    host_nodes = None   # This is a list of node objects that represent spots
                        # Nodes are added as they connect for the first time
    
    """ Initialization """
    def __init__(self, name):
        self.host_name = name
        self.host_nodes = []
        print("New Empty Parking Lot Created...")
    
    """ Member Functions """
    def add_node(self, node):
        if type(node) is PNode:
            self.host_nodes.append(node)
        else:
            print("Object not a node...")
    
    """ Getters and Setters """
    def set_id(self, id):
        self.host_id = id
    def get_id(self):
        return self.host_id
    
    def set_name(self, name):
        self.host_name = name
    def get_name(self):
        return self.host_name
    
    def get_nodes(self):
        return self.host_nodes
"""-----------------------------------------------"""    

"""
This class defines an object that represents a single parking space node.
The host node software will maintain a list of these objects to allow it
to track its child nodes.
"""

class PNode:    

    """ Variables """
    host = None
    node_id = None          # Identification number of the node
    node_ipAddr = None      # IP Address of the node
    node_lastConn = None    # String representing time of last connection
    node_inUse = None      # Boolean value representing if the spot is taken
    node_disabled = None

    """ Initialization """
    def __init__(self, id, ipAddr, host):
        self.host = host
        self.node_id = id
        self.node_ipAddr = ipAddr
        self.node_inUse = False
        self.node_disabled = False
        self.node_lastConn = datetime.now()
        print("New node object created...")

    """ Member Functions """
    def get_info(self):
        return "ID: " + str(self.node_id) + " | IP: " + str(self.node_ipAddr) + " | Status: " + str(self.node_inUse)

    """ Getters and Setters """
    def get_host(self):
        return self.host
    def set_host(self, host):
        self.host = host
        
    def get_id(self):
        return self.node_id
    def set_id(self, id):
        self.node_id = id
        
    def get_ip(self):
        return self.node_ipAddr
    def set_ip(self, ip):
        self.node_ipAddr = ip
        
    def get_last_connection(self):
        return self.node_lastConn
    def set_last_connection(self, time):
        self.node_lastConn = time
        
    def get_inUse(self):
        return self.node_inUse
    def set_inUse(self, status):
        self.node_inUse = status
        
    def get_disabled(self):
        return self.node_disabled
    def set_disabled(self, disabled):
        self.node_disabled = disabled
