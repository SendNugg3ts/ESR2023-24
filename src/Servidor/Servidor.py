import socket
import threading
from Servidor.ServerWorker import ServerWorker

# Variable to track streaming state and the current streaming port
is_streaming = False
current_streaming_port = None

def find_available_port(start_port):
    # Function to find an available port starting from the specified port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', start_port))
                return start_port
            except socket.error:
                start_port += 1

def StartStreaming(ServerIP, start_port):
    global is_streaming, current_streaming_port
    
    # Check if streaming is already in progress
    if is_streaming:
        print("Streaming is already in progress.")
        return

    streaming_port = find_available_port(start_port)
    
    rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtspSocket.bind((ServerIP, streaming_port))
    rtspSocket.listen(5)
    print(f"Servidor aguardando conexões em {ServerIP}:{streaming_port}")
    
    is_streaming = True
    current_streaming_port = streaming_port
    
    while True:
        print("a streamar")
        clientInfo = {}
        clientInfo['rtspSocket'] = rtspSocket.accept()
        ServerWorker(clientInfo).run()

    # Reset streaming state and current streaming port when streaming ends
    is_streaming = False
    current_streaming_port = None
    rtspSocket.close()

# Função para lidar com um cliente
def handle_client(client_socket, ServerIP, start_port):
    global is_streaming, current_streaming_port
    
    message = client_socket.recv(1024)
    print(f"Recebido do cliente {threading.current_thread().name}: {message.decode()}")
    if message.decode() == "START_STREAM":
        print("A começar stream")
        StartStreaming(ServerIP, start_port)
    else:
        response = "HELLO"
        client_socket.send(response.encode())
    
# Criar um socket do servidor
def serverStart(host, port, start_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor aguardando conexões em {host}:{port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão aceite de {client_address[0]}:{client_address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,host, start_port))
        client_handler.start()

	


