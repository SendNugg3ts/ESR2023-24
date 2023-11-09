import socket
import time
import json
import sys
import os
import re


from Servidor.Servidor import *
from Cliente.Cliente import *

nodeID = sys.argv[1]

current_pwd_path = os.path.dirname(os.path.abspath(__file__))
video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
path_to_nodeID = os.path.join(video_pwd_path, "util/" + str(nodeID) + ".json")


i = open(path_to_nodeID)

info = json.load(i)

if bool(info["RP"]) == True:
    nodeIP = info["ip"]
    server1IP = info["vizinhos"][0]["ip"]
    server2IP = info["vizinhos"][1]["ip"]
    nodePort = info["porta"]
elif bool(info["RP"]) == False and bool(info["router"]) == True:
    nodeIP = info["ip"]
    clienteEIP = info["vizinhos"][0]["ip"]
    clienteDIP = info["vizinhos"][1]["ip"]
    nodePort = info["porta"]



filename = "movie.Mjpeg"
SERVERPORT = 2500
if isServer:
    StartStreaming(nodeIP, SERVERPORT)
else:
    clientGuiStart(hostIP, SERVERPORT, nodeIP, 3500, nodeID, filename)







