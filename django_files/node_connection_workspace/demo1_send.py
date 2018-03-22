"""
This is the code that will simulate the host for our first demo.
It will wait for a message from the node then broadcast it to
the server.
"""

from networking import WebConnection
from host_node import PNode, PHost

def main():
    """ Create an object to represent this parking spot """
    this_host = PHost( "Summit Hall Lot")
    test_node = PNode (1, "192.168.1.2", 1)
    test_node.set_inUse(True)
    this_host.add_node(test_node)
    
    """ Create an object to broadcoast updates to host """
    host_connection = WebConnection("127.0.0.1", 12345)
    host_connection.init_conn()
    
    """ Create an object to recieve data from sensor """
    # gpio_connection = 

    # while True:
    """ Wait for updates from sensor """
        
    """ Broadcast to Host """
    host_connection.transmit_object(this_host)

        
main()
