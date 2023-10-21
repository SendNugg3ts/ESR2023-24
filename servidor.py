import socket

# Defina o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substitua pelo IP do servidor
port = 10000  # Substitua pela porta desejada

# Crie um socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associe o socket ao endereço e à porta
server_socket.bind((host, port))

# Espere por uma conexão
server_socket.listen(1)

print(f"Servidor aguardando conexão em {host}:{port}")

# Aceite a conexão quando um cliente se conectar
client_socket, client_address = server_socket.accept()

while True:
    # Receba uma mensagem do cliente
    message = client_socket.recv(1024)

    # Verifique se a mensagem é "fim" (para encerrar a comunicação)
    if message.decode() == "fim":
        break

    # Imprima a mensagem recebida do cliente
    print(f"Recebido do cliente: {message.decode()}")

    # Envie uma resposta de volta ao cliente
    response = input("Digite uma resposta: ")  # Aguarde a entrada do servidor
    client_socket.send(response.encode())

# Fechar a conexão com o cliente
client_socket.close()

# Fechar o socket do servidor
server_socket.close()

