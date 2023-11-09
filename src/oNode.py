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
    server1Port = info["vizinhos"][0]["porta"]
    server2IP = info["vizinhos"][1]["ip"]
    server2Port = info["vizinhos"][1]["porta"]
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

def RpTestLatency(host1,port1,host2,port2):
    client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            start = time.time()
            client_socket1.connect((host1, port1))
            message = "Time test"
            client_socket1.send(message.encode())

            response = client_socket1.recv(1024)
            print(f"Recebido do {host1}: {response.decode()}")
            end = time.time()
            latencia1=end-start
        except:
            pass
        try:
            start = time.time()
            client_socket2.connect((host2, port2))
            message = "Time test"
            client_socket2.send(message.encode())

            response = client_socket2.recv(1024)
            print(f"Recebido do {host2}: {response.decode()}")
            end = time.time()
            latencia2= end-start
        except:
            pass
        try:
            if latencia1 >= latencia2:
                print("Servidor 2 mais rapido")
                server = "servidor2"
            else:
                print("Servidor 1 mais rapido")
                server = "servidor1"
        except:
            continue
        sleep(20)
    client_socket1.close()
    client_socket2.close()



if bool(info["server"]) == True:#Servidor
    serverStart(nodeIP,nodePort)
elif bool(info["router"]) == False and bool(info["server"]) == False:#Cliente cabou
    clientGuiStart(routerIP, routerPort, nodeIP, nodePort, nodeID, filename)
elif bool(info["RP"]) == False and bool(info["router"]) == True:#Router
    pass
elif bool(info["RP"]) == True:#RP
    RpTestLatency(server1IP,server1Port,server2IP,server2Port)
else:
    raise ValueError("Node type not supported")







