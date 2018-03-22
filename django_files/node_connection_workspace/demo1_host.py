"""
This is the code that will simulate the host for our first demo.
It will wait for a message from the node then broadcast it to
the server.
"""

from networking import MeshConnection
from host_node import PHost, PNode
from sqlconnection import *

def main():

    """ Creates a way of interacting with the local sql database """
    sql_controller = SQLController("mysql://myprojectuser:password@localhost/myproject")

    """ Creates a way of listening for messages from the node """
    #mesh_connection = MeshConnection("192.168.2.1", 12345)
    #mesh_connection.init_conn()

    """ Creates a way of broadcasting messages to the server """
    host_connection = MeshConnection("127.0.0.1", 12345)
    host_connection.init_conn()

    while True:
        """ Wait for object to be sent from a node """
        obj = host_connection.listen()

        """ Relay data to the server """
        if type(obj) is PHost:
            sql_controller.set_host_status(obj)
            print("Host recieved")
        else:
            print("Recieved garbage from host")
main()
