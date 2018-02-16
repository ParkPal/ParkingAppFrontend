from networking import WebConnection
from sqlconnection import SQLController
from host import Host
from node import Node

"""
sql_contoller = SQLController("sqlite:///home/bxavier/capstoneFE/virtualenvs/virtualenvs/djangodev/Old/mysite/db.sqlite3")
se_connection = WebConnection("127.0.0.1", 12345)
se_connection.init_conn()
"""

sql_contoller = SQLController("sqlite:///home/bxavier/capstoneFE/virtualenvs/virtualenvs/djangodev/Old/mysite/db.sqlite3")
server_conn = WebConnection("127.0.0.1", 12345)
server_conn.init_conn()

nd = Node


server_conn.transmit_object(nd)


"""
while True:
    obj = se_connection.listen()
    if type(obj) is Node:
        db_conn.add_node(obj)
    else:
        print("Recieved garbage from node")
"""
"""main()"""

