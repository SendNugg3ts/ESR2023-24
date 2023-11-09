import socket
import time
import json
import sys
import os
import re


from Servidor.Servidor import *
from Cliente.Cliente import *

nodeID = sys.argv[1]

filename = "movie.Mjpeg"

current_pwd_path = os.path.dirname(os.path.abspath(__file__))
video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
path_to_nodeID = os.path.join(video_pwd_path, "util/" + str(nodeID) + ".json")


i = open(path_to_nodeID)

info = json.load(i)

if bool(info["RP"]) == True:#RP
    nodeIP = info["ip"]
    server1IP = info["vizinhos"][0]["ip"]
    server2IP = info["vizinhos"][1]["ip"]
    router1IP = info["vizinhos"][2]["ip"]
    router2IP = info["vizinhos"][3]["ip"]
    nodePort = info["porta"]
elif bool(info["RP"]) == False and bool(info["router"]) == True:#Router
    nodeIP = info["ip"]
    clienteEIP = info["vizinhos"][0]["ip"]
    clienteDIP = info["vizinhos"][1]["ip"]
    routerVizinhoID = info["vizinhos"][2]["ip"]
    RPID =info["vizinhos"][3]["ip"]
    nodePort = info["porta"]
elif bool(info["server"]) == True:#Servidor
    nodeIP = info["ip"]
    RPIP = info["vizinhos"][0]["ip"]
    nodePort = info["porta"]
elif bool(info["router"]) == False and bool(info["server"]) == False:#Cliente
    nodeIP = info["ip"]
    routerIP = info["vizinhos"][0]["ip"]
    routerPort = info["vizinhos"][0]["porta"]
    nodePort = info["porta"]


if bool(info["server"]) == True:#Servidor
    StartStreaming(nodeIP, nodePort)
elif bool(info["router"]) == False and bool(info["server"]) == False:#Cliente
    clientGuiStart(routerIP, routerPort, nodeIP, nodePort, nodeID, filename)
elif bool(info["RP"]) == False and bool(info["router"]) == True:#Router
    pass
elif bool(info["RP"]) == True:#RP
    pass
else:
    raise ValueError("Node type not supported")







