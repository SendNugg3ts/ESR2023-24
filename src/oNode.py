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
        rp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start = time.time()
        print(f"Conectar-se a {host1}:{port1_mensagem}")
        rp_socket1.connect((host1, port1_mensagem))
        message = "Time test"
        rp_socket1.send(message.encode())
        response = rp_socket1.recv(1024)
        print(f"Received from {host1}: {response.decode()}")
        end = time.time()
        latencia1 = end - start
        rp_socket1.close()
    except Exception as e:
        print(f"Error with path 1: {e}")
        latencia1 = float('inf')  # Set a high latency value in case of an error

    try:
        rp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start = time.time()
        print(f"Conectar-se a {host2}:{port2_mensagem}")
        rp_socket2.connect((host2, port2_mensagem))
        message = "Time test"
        rp_socket2.send(message.encode())

        response = rp_socket2.recv(1024)
        print(f"Received from {host2}: {response.decode()}")
        end = time.time()
        latencia2 = end - start
        rp_socket2.close()
    except Exception as e:
        print(f"Error with path 2: {e}")
        latencia2 = float('inf')  # Set a high latency value in case of an error
        
    rp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if latencia1 < latencia2:
        print("Path 1 is faster")
        rp_socket1.connect((host1, port1_mensagem))
        rp_socket2.connect((host2, port2_mensagem))
        rp_socket1.send("START_STREAM".encode())
        rp_socket2.send("LENTOOOO".encode())
        rp_socket1.close()
        rp_socket2.close()
        return host1
    else:
        print("Path 2 is faster")
        rp_socket1.connect((host1, port1_mensagem)) 
        rp_socket2.connect((host2, port2_mensagem))
        rp_socket1.send("LENTOOOO".encode()) 
        rp_socket2.send("START_STREAM".encode())
        rp_socket1.close()
        rp_socket2.close()
        return host2



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
        fasterIpRP=RpTestLatency(vizinhos_ip[3],vizinhos_porta_mensagem[3],vizinhos_ip[2],vizinhos_porta_mensagem[2])
        client_socket.send(fasterIpRP.encode('utf-8'))
        client_socket.close()
        break
    
def mensagem_rp_router():
    RP_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RP_socket_1.bind((nodeIP3, nodePort1_mensagem))
    RP_socket_1.listen(20)
    RP_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RP_socket_2.bind((nodeIP4, nodePort1_mensagem))
    RP_socket_2.listen(20)
    print(f"RP aguardando conexões em {nodeIP3}:{nodePort1_mensagem}")
    print(f"RP aguardando conexões em {nodeIP4}:{nodePort1_mensagem}")
    while True:
        rp_socket1, client_address1 = RP_socket_1.accept()
        
        print(f"Conexão aceita de {client_address1}")
        mensagem_cliente1 = rp_socket1.recv(1024).decode('utf-8')
        print(f"Mensagem recebida no socket 1: {mensagem_cliente1}")

        resposta1 = "Resposta RP no socket 1"
        rp_socket1.send(resposta1.encode('utf-8'))
        
        rp_socket2, client_address2 = RP_socket_2.accept()
        
        print(f"Conexão aceita de {client_address2}")
        mensagem_cliente2 = rp_socket2.recv(1024).decode('utf-8')
        print(f"Mensagem recebida no socket 2: {mensagem_cliente2}")
        
        resposta2 = "Resposta RP no socket 2"
        rp_socket2.send(resposta2.encode('utf-8'))
                
        path1 = rp_socket1.recv(1024).decode('utf-8')
        if path1:
            print("ok foi o nodeIP3")
            return nodeIP3
        path2 = rp_socket2.recv(1024).decode('utf-8')
        if path2:
            print("ok foi o nodeIP4")
            return nodeIP4
        else:
            Exception("Error connecting")



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
    fastest_path=mensagem_rp_router()

    StartStreaming(fastest_path,nodePort_streaming)
    









