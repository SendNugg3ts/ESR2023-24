import socket
import threading
from Servidor.ServerWorker import ServerWorker

# Função para lidar com um cliente
def handle_client(client_socket):
    message = client_socket.recv(1024)
    print(f"Recebido do cliente {threading.current_thread().name}: {message.decode()}")
    response = "HELLO"
    client_socket.send(response.encode())
    client_socket.close()

# Criar um socket do servidor
def serverStart(host,port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor aguardando conexões em {host}:{port}")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão aceite de {client_address[0]}:{client_address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
	
	
def StartStreaming(ServerIP, ServerPort):
    rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtspSocket.bind((ServerIP, ServerPort))
    rtspSocket.listen(5)
    print(f"Servidor aguardando conexões em {ServerIP}:{ServerPort}")
    # Receive client info (address, port) through RTSP/TCP session
    while True:
        clientInfo = {}
        clientInfo['rtspSocket'] = rtspSocket.accept()
        ServerWorker(clientInfo).run()
    rtspSocket.close()


