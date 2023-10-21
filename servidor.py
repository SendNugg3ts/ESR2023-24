import socket

# Defina o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substitua pelo IP do seu servidor
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

# Envie a mensagem "HELLO" para o cliente
message = "HELLO"
client_socket.send(message.encode())

# Feche a conexão com o cliente
client_socket.close()

# Feche o socket do servidor
server_socket.close()
