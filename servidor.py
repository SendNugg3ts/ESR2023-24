import socket

# Definir o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substitua pelo IP do servidor
port = 10000  # Substitua pela porta desejada

# Criar um socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associar o socket ao endereço e à porta
server_socket.bind((host, port))

# Esperar por uma conexão
server_socket.listen(1)

print(f"Servidor aguardando conexão em {host}:{port}")

# Aceitar a conexão quando um cliente se conectar
client_socket, client_address = server_socket.accept()

while True:
    # Receber uma mensagem do cliente
    message = client_socket.recv(1024)

    # Verificar se a mensagem é "fim" (para terminar a comunicação)
    if message.decode() == "fim":
        break

    # Imprimir a mensagem recebida do cliente
    print(f"Recebido do cliente: {message.decode()}")

    # Enviar uma resposta de volta ao cliente
    response = input("Digite uma resposta: ")  # Aguarde a entrada do servidor
    client_socket.send(response.encode())

# Fechar a conexão com o cliente
client_socket.close()

# Fechar o socket do servidor
server_socket.close()

