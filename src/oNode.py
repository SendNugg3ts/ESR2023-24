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

if bool(info["RP"]) != True and bool(info["router"]) == False:
    nodeIP = info["ip"]

elif bool(info["RP"]) == True:
    nodeIP1 = info["ip1"]
    nodeIP2 = info["ip2"]
    nodeIP3 = info["ip3"]
    nodeIP4 = info["ip4"]

else:
    nodeIP1 = info["ip1"]
    nodeIP2 = info["ip2"]
    nodeIP3 = info["ip3"]
    

nodePort_streaming = info["porta_streaming"]
nodePort1_mensagem = info["porta_mensagem"]
vizinhos_ip, vizinhos_porta_streaming, vizinhos_porta_mensagem = [], [], []
for i in range(len(info["vizinhos"])):
    ip = info["vizinhos"][i]["ip"]
    porta_streaming = info["vizinhos"][i]["porta_streaming"]
    porta_mensagem = info["vizinhos"][i]["porta_mensagem"]
    vizinhos_ip.append(ip)
    vizinhos_porta_streaming.append(porta_streaming)
    vizinhos_porta_mensagem.append(porta_mensagem)


def RPConfirmation(server_socket):
        stream_data = server_socket.recv(20480)
        if stream_data:
            print(stream_data)
            #print("Stream data received!")
        


def RpTestLatency(host1, port1_mensagem, host2, port2_mensagem):
    try:
        client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start = time.time()
        client_socket1.connect((host1, port1_mensagem))
        message = "Time test"
        client_socket1.send(message.encode())

        response = client_socket1.recv(1024)
        print(f"Received from {host1}: {response.decode()}")
        end = time.time()
        latencia1 = end - start
        client_socket1.close()
    except Exception as e:
        print(f"Error with path 1: {e}")
        latencia1 = float('inf')  # Set a high latency value in case of an error

    try:
        client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start = time.time()
        client_socket2.connect((host2, port2_mensagem))
        message = "Time test"
        client_socket2.send(message.encode())

        response = client_socket2.recv(1024)
        print(f"Received from {host2}: {response.decode()}")
        end = time.time()
        latencia2 = end - start
        client_socket2.close()
    except Exception as e:
        print(f"Error with path 2: {e}")
        latencia2 = float('inf')  # Set a high latency value in case of an error
        
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if latencia1 < latencia2:
        print("Path 1 is faster")
        server_socket.connect((host1, port1_mensagem))
        server_socket.send("START_STREAM".encode())
        server_socket.close()
        return host1
    else:
        print("Path 2 is faster")
        server_socket.connect((host2, port2_mensagem)) 
        server_socket.send("START_STREAM".encode())
        server_socket.close()
        return host2




def verificar_se_vizinho_tem_streaming(vizinho_ip, vizinho_porta):
    buffer_size = 1024
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((vizinho_ip, vizinho_porta))
            s.sendall(b"CHECK_STREAMING_STATUS")
            response = s.recv(buffer_size).decode("utf-8")
            if response == "STREAMING_AVAILABLE":
                return True
            else:
                return False
    except socket.error as e:
        print(f"Erro de conexão com o vizinho: {e}")
        return False


def mensagem_cliente_router(routerIP,routerPort):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((routerIP, routerPort))
    cliente_socket.send("SEND STREAM".encode())
    RPIP = cliente_socket.recv(1024).decode()
    return RPIP

def mensagem_router_cliente():
    router_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    router_socket.bind((nodeIP3, nodePort1_mensagem))
    router_socket.listen(5)
    print(f"Router aguardando conexões em {nodeIP3}:{nodePort1_mensagem}")
    while True:
        client_socket, client_address = router_socket.accept()
        print(f"Conexão aceite de {client_address}")
        mensagem_cliente = client_socket.recv(1024).decode('utf-8')
        print(f"Mensagem recebida: {mensagem_cliente}")
        fasterIpRP=RpTestLatency(vizinhos_ip[2],vizinhos_porta_mensagem[2],vizinhos_ip[3],vizinhos_porta_mensagem[3])
        client_socket.send(fasterIpRP.encode('utf-8'))
        client_socket.close()
        break


if bool(info["server"]) == True:#Servidor
    nodeType= "server"
    serverStart(nodeIP,nodePort1_mensagem,nodePort_streaming)

elif bool(info["router"]) == False and bool(info["server"]) == False:#Cliente cabou
    RPIP=mensagem_cliente_router(vizinhos_ip[0],vizinhos_porta_mensagem[0])
    clientGuiStart(RPIP, 3000, nodeIP, nodePort_streaming, nodeID, filename)
    

elif bool(info["RP"]) == False and bool(info["router"]) == True:  # Router
    nodeType = "router"
    mensagem_router_cliente()

elif bool(info["RP"]) == True:  # RP
    nodeType = "RP"
    try:
        RpTestLatency(vizinhos_ip[0], vizinhos_porta_mensagem[0], vizinhos_porta_streaming[0], vizinhos_ip[1], vizinhos_porta_mensagem[1], vizinhos_porta_streaming[1], nodePort_streaming)
    except Exception as e:
        print(f"Erro ao testar latência para servidores: {e}")
else:
    raise ValueError("Node type not supported")









