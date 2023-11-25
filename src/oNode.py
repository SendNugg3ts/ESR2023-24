import socket
import time
import json
import sys
import os
import re
import select

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




#Routers usam para ver o mais raido
def RpTestLatency(host1, port1_mensagem, host2, port2_mensagem,isRouter,checkingRouter,host3,port3_mensagem):
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
        if checkingRouter:
            rp_socket1.connect((host3, port3_mensagem))
        else:  
            rp_socket1.connect((host1, port1_mensagem))
        rp_socket2.connect((host2, port2_mensagem))
        rp_socket1.send("START_STREAM".encode())
        rp_socket2.send("Slower".encode())
        if isRouter: 
            response = rp_socket1.recv(1024).decode()#problema aqui é quando ele conecta se a outro router, a resposta do outro router é sim porque ele não se conecta ao RP
            rp_socket1.close()
            rp_socket2.close()
            return response
        else:
            rp_socket1.close()
            rp_socket2.close()
            return host1
    else:
        print("Path 2 is faster")
        rp_socket1.connect((host1, port1_mensagem)) 
        rp_socket2.connect((host2, port2_mensagem))
        rp_socket1.send("Slower".encode()) 
        rp_socket2.send("START_STREAM".encode())
        if isRouter:
            response = rp_socket2.recv(1024).decode()
            rp_socket1.close()
            rp_socket2.close()
            return response
        else:
            rp_socket1.close()
            rp_socket2.close()
            return host2


#Parte Cliente
def mensagem_cliente_router(routerIP,routerPort):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((routerIP, routerPort))
    cliente_socket.send("SEND STREAM".encode())
    RPIP = cliente_socket.recv(1024).decode()
    return RPIP

#Parte Router
def mensagem_router_cliente():
    router_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    router_socket_1.bind((nodeIP3, nodePort1_mensagem))
    router_socket_1.listen(6)

    router_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    router_socket_2.bind((nodeIP2, nodePort1_mensagem))
    router_socket_2.listen(6)

    inputs = [router_socket_1, router_socket_2]
    print(f"Router aguardando conexões em {nodeIP3}:{nodePort1_mensagem}")
    passar_streaming = False
    fasterIpRP = "nada"
    while True:
        readable, _, _ = select.select(inputs, [], [])

        for readable_socket in readable:
            if readable_socket == router_socket_1:
                client_socket, client_address = router_socket_1.accept()
                print(f"Conexão aceite de {client_address}")
                mensagem_cliente = client_socket.recv(1024).decode()
                print(f"Mensagem recebida: {mensagem_cliente}")

            elif readable_socket == router_socket_2:
                router_socket, client_address = router_socket_2.accept()
        


        if client_address[0] != vizinhos_ip[4]:
            if passar_streaming == False:
                stream_test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                stream_test_socket.connect((vizinhos_ip[4], vizinhos_porta_mensagem[4]))
                stream_test_socket.send("Estás a passar streaming?".encode())
                resposta_streaming = stream_test_socket.recv(1024).decode()
                if resposta_streaming == "sim":
                    fasterIpRP=RpTestLatency(vizinhos_ip[4],vizinhos_porta_mensagem[4],vizinhos_ip[2],vizinhos_porta_mensagem[2],True,True,vizinhos_ip[3],vizinhos_porta_mensagem[3])
                    passar_streaming = True
                else:
                    fasterIpRP=RpTestLatency(vizinhos_ip[3],vizinhos_porta_mensagem[3],vizinhos_ip[2],vizinhos_porta_mensagem[2],True,False,None,None)
                    passar_streaming = True
            stream_test_socket.close()

            client_socket.send(fasterIpRP.encode())
            client_socket.close()

        else:
            if passar_streaming == False:
                router_socket.send("não".encode())
            else:
                router_socket.send("sim".encode())
            
        
    router_socket_1.close()
    router_socket_2.close()
        
#Parte do RP
def handle_client(rp_socket, client_address):
    print(f"Conexão aceita de {client_address}")
    mensagem_cliente = rp_socket.recv(1024).decode()
    print(f"Mensagem recebida: {mensagem_cliente}")

    if mensagem_cliente == "START_STREAM":
        print(f"OK foi de {client_address}")
        fastest_server=RpTestLatency(vizinhos_ip[0],vizinhos_porta_mensagem[0],vizinhos_ip[1],vizinhos_porta_mensagem[1],False,False,None,None)
        rp_socket.send(fastest_server.encode())

    rp_socket.close()
    
    
def mensagem_rp_router():
    RP_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RP_socket_1.bind((nodeIP3, nodePort1_mensagem))
    RP_socket_1.listen(20)

    RP_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RP_socket_2.bind((nodeIP4, nodePort1_mensagem))
    RP_socket_2.listen(20)

    print(f"RP aguardando conexões em {nodeIP3}:{nodePort1_mensagem}")
    print(f"RP aguardando conexões em {nodeIP4}:{nodePort1_mensagem}")

    inputs = [RP_socket_1, RP_socket_2]

    while True:
        # Use select to wait for incoming connections
        readable, _, _ = select.select(inputs, [], [])

        for readable_socket in readable:
            if readable_socket == RP_socket_1:
                rp_socket1, client_address1 = RP_socket_1.accept()
                thread1 = threading.Thread(target=handle_client, args=(rp_socket1, client_address1))
                thread1.start()

            elif readable_socket == RP_socket_2:
                rp_socket2, client_address2 = RP_socket_2.accept()
                thread2 = threading.Thread(target=handle_client, args=(rp_socket2, client_address2))
                thread2.start()




if bool(info["server"]) == True:#Servidor
    nodeType= "server"
    serverStart(nodeIP,nodePort1_mensagem,nodePort_streaming)

elif bool(info["router"]) == False and bool(info["server"]) == False:#Cliente cabou
    serverIP=mensagem_cliente_router(vizinhos_ip[0],vizinhos_porta_mensagem[0])
    clientGuiStart(serverIP, 3000, nodeIP, nodePort_streaming, nodeID, filename)
    

elif bool(info["RP"]) == False and bool(info["router"]) == True:  # Router
    nodeType = "router"
    mensagem_router_cliente()

elif bool(info["RP"]) == True:  # RP
    nodeType = "RP"
    mensagem_rp_router()
    









