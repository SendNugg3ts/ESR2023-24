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

if bool(info["RP"]) != True:
    nodeIP = info["ip"]
elif bool(info["RP"]) == True:
    nodeIP1 = info["ip1"]
    nodeIP2 = info["ip2"]
    nodeIP3 = info["ip3"]
    nodeIP4 = info["ip4"]

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
        


def RpTestLatency(host1, port1_mensagem, port1_streaming, host2, port2_mensagem, port2_streaming, rpPort_streaming):
    while True:
        try:
            # Create a socket for server 1
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
            print(f"Error with server 1: {e}")
            latencia1 = float('inf')  # Set a high latency value in case of an error

        try:
            # Create a socket for server 2
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
            #time.sleep(2)
        except Exception as e:
            print(f"Error with server 2: {e}")
            latencia2 = float('inf')  # Set a high latency value in case of an error
            
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if latencia1 < latencia2:
            print("Server 1 is faster")
            server_socket.connect((host1, port1_mensagem))
            server_socket.send("START_STREAM".encode())
            clientGuiStart(host1,port1_streaming,nodeIP1,rpPort_streaming,nodeID,filename)#4010 tem de ser a porta de streaming do server e 3000 tem de ser a porta que recebe os rtsps
        else:
            print("Server 2 is faster")
            server_socket.connect((host2, port2_mensagem)) 
            server_socket.send("START_STREAM".encode())
            #time.sleep(3)
            clientGuiStart(host2,port2_streaming,nodeIP2,rpPort_streaming,nodeID,filename)          
        #print(f"Latency for server 1: {latencia1} seconds")
        #print(f"Latency for server 2: {latencia2} seconds")
        server_socket.close()
        time.sleep(20)



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




if bool(info["server"]) == True:#Servidor
    nodeType= "server"
    serverStart(nodeIP,nodePort1_mensagem,nodePort_streaming)

elif bool(info["router"]) == False and bool(info["server"]) == False:#Cliente cabou
    clientGuiStart(vizinhos_ip[0], vizinhos_porta_streaming[0], nodeIP, nodePort_streaming, nodeID, filename)
    

elif bool(info["RP"]) == False and bool(info["router"]) == True:  # Router
    nodeType = "router"
    try:
        print(f"Tentando conectar ao Vizinho: {vizinhos_ip[2]}:{vizinhos_porta_mensagem[2]}")
        vizinho_tem_streaming = verificar_se_vizinho_tem_streaming(vizinhos_ip[2], vizinhos_porta_mensagem[2])
        print(f"Verificando streaming: {vizinho_tem_streaming}")

        if vizinho_tem_streaming:
            print(f"Conectando ao Vizinho para Streaming: {vizinhos_ip[2]}:{vizinhos_porta_streaming[2]}")
            clientGuiStart(vizinhos_ip[2], vizinhos_porta_streaming[2], nodeIP, nodePort_streaming, nodeID, filename)
        else:
            print(f"Conectando ao RP: {vizinhos_ip[-1]}:{vizinhos_porta_streaming[-1]}")
            clientGuiStart(vizinhos_ip[-1], vizinhos_porta_streaming[-1], nodeIP, nodePort_streaming, nodeID, filename)

        print("Conexão estabelecida com sucesso.")
    except Exception as e:
        print(f"Erro ao conectar ao RP ou Vizinho: {e}")


elif bool(info["RP"]) == True:  # RP
    nodeType = "RP"
    try:
        RpTestLatency(vizinhos_ip[0], vizinhos_porta_mensagem[0], vizinhos_porta_streaming[0], vizinhos_ip[1], vizinhos_porta_mensagem[1], vizinhos_porta_streaming[1], nodePort_streaming)
    except Exception as e:
        print(f"Erro ao testar latência para servidores: {e}")
else:
    raise ValueError("Node type not supported")









