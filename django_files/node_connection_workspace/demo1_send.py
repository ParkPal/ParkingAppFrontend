"""
This is the code that will simulate the host for our first demo.
It will wait for a message from the node then broadcast it to
the server.
"""

from networking import WebConnection
from host import Host
from node import Node

def main():
    """ Create an object to represent this parking spot """
    this_host = Host( "Summit Hall Lot")
    test_node = Node (1, "192.168.1.2")
    test_node.set_inUse(False)
    this_host.add_node(test_node)
    
    """ Create an object to broadcoast updates to host """
    host_connection = WebConnection("192.168.1.39", 12345)
    host_connection.init_conn()
    
    """ Create an object to recieve data from sensor """
    # gpio_connection = 

    # while True:
    """ Wait for updates from sensor """
        
    """ Broadcast to Host """
    host_connection.transmit_object(this_host)

        
main()
