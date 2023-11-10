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
    clienteEPorta = info["vizinhos"][0]["porta"]
    clienteDIP = info["vizinhos"][1]["ip"]
    clienteDPorta = info["vizinhos"][1]["porta"]
    routerVizinhoID = info["vizinhos"][2]["ip"]
    routerVizinhoPorta = info["vizinhos"][2]["porta"]
    RPID =info["vizinhos"][3]["ip"]
    RPPorta =info["vizinhos"][3]["porta"]
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

def RPConfirmation(server_socket):
        stream_data = server_socket.recv(20480)
        if stream_data:
            print("Stream data received!")


def RpTestLatency(host1, port1, host2, port2):
    while True:
        try:
            # Create a socket for server 1
            client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            start = time.time()
            client_socket1.connect((host1, port1))
            message = "Time test"
            client_socket1.send(message.encode())

            response = client_socket1.recv(1024)
            print(f"Received from {host1}: {response.decode()}")
            end = time.time()
            latencia1 = end - start
            client_socket1.close()
        except Exception as e:
            print(f"Error with server 1: {e}")
            latencia1 = float('inf')  # Set a high latency value in case of an error

        try:
            # Create a socket for server 2
            client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            start = time.time()
            client_socket2.connect((host2, port2))
            message = "Time test"
            client_socket2.send(message.encode())

            response = client_socket2.recv(1024)
            print(f"Received from {host2}: {response.decode()}")
            end = time.time()
            latencia2 = end - start
            client_socket2.close()
            time.sleep(2)
        except Exception as e:
            print(f"Error with server 2: {e}")
            latencia2 = float('inf')  # Set a high latency value in case of an error
            
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if latencia1 < latencia2:
            print("Server 1 is faster")
            server_socket.connect((host1, port1))

        else:
            print("Server 2 is faster")
            server_socket.connect((host2, port2))
            
        server_socket.send("START_STREAM".encode())
        print(f"Latency for server 1: {latencia1} seconds")
        print(f"Latency for server 2: {latencia2} seconds")
        RPConfirmation(server_socket)
        server_socket.close()
        time.sleep(20)





if bool(info["server"]) == True:#Servidor
    nodeType= "server"
    serverStart(nodeIP,nodePort,4010)
elif bool(info["router"]) == False and bool(info["server"]) == False:#Cliente cabou
    clientGuiStart(routerIP, routerPort, nodeIP, nodePort, nodeID, filename)
elif bool(info["RP"]) == False and bool(info["router"]) == True:#Router
    nodeType = "router"
elif bool(info["RP"]) == True:#RP
    nodeType = "RP"
    RpTestLatency(server1IP,server1Port,server2IP,server2Port)
else:
    raise ValueError("Node type not supported")







