"""
This is the code that will simulate the host for our first demo.
It will wait for a message from the node then broadcast it to
the server.
"""

from networking import MeshConnection
from host import Host
from node import Node
from sqlconnection import *

def main():

    """ Creates a way of interacting with the local sql database """
    sql_controller = SQLController('mysql://myprojectuser:password@localhost/myproject')

    """ Creates a way of listening for messages from the node """
    #mesh_connection = MeshConnection("192.168.2.1", 12345)
    #mesh_connection.init_conn()

    while True:
        """ Wait for object to be sent from a node """
        host_connection = MeshConnection("192.168.1.39", 12345)
        host_connection.init_conn()

        obj = host_connection.listen()

        """ Relay data to the server """
        if type(obj) is Host:
            i = 0
            sql_controller.set_host_status(obj)
            print("Debug Diagnostics: ")
            print("Host Lot Name: " + obj.get_name())
            print("Host Node Count" + str(len(obj.get_nodes())))
            print("Host recieved")
            print("Nodes:")
            for node in obj.get_nodes():
                print("Node number: " + str(i))
                print(node.get_info())
        else:
            print("Recieved garbage from host")
        host_connection.close_conn()
main()
