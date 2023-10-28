import socket
import threading

# Definir o endereço IP e a porta do servidor
#host = '10.0.0.10'  # Substitua pelo IP do servidor
#port = 10000  # Substituir pela porta desejada

# Função para lidar com um cliente
def handle_client(client_socket):
    # Receber uma mensagem do cliente
    message = client_socket.recv(1024)

    # Imprimir a mensagem recebida do cliente
    print(f"Recebido do cliente {threading.current_thread().name}: {message.decode()}")

    # Enviar uma resposta de volta ao cliente
    response = "HELLO"
    client_socket.send(response.encode())

    # Fechar a conexão com o cliente
    client_socket.close()

# Criar um socket do servidor
def serverStart(host,port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associar o socket ao endereço e à porta
    server_socket.bind((host, port))

    # Esperar por conexões de clientes (pode ter no max 5)
    server_socket.listen(5)

    print(f"Servidor aguardando conexões em {host}:{port}")

    while True:
        # Aceitar a conexão quando um cliente se conectar
        client_socket, client_address = server_socket.accept()
        print(f"Conexão aceite de {client_address[0]}:{client_address[1]}")

        # Iniciar uma nova thread para lidar com o cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()



