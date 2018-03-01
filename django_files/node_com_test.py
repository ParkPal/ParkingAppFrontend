from networking import MeshConnection
from sqlconnection import SQLController
from host import Host
from node import Node


sql_contoller = SQLController("sqlite:///home/bxavier/capstoneFE/virtualenvs/virtualenvs/djangodev/Old/mysite/db.sqlite3")
ls_connection = MeshConnection("0.0.0.0", 12345)
ls_connection.init_conn()

while True:
    obj = ls_connection.listen()
    if type(obj) is Node:
        sql_contoller.add_node(obj)
    else:
        print("Recieved garbage from node")

main()
