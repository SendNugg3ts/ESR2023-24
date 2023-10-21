import socket

# Definir o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substituir pelo IP do servidor
port = 10000  # Substitua pela porta desejada

# Criar um socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associar o socket ao endereço e à porta
server_socket.bind((host, port))

# Espere por uma conexão
server_socket.listen(1)

print(f"Servidor aguardando conexão em {host}:{port}")

# Aceitar a conexão quando um cliente se conectar
client_socket, client_address = server_socket.accept()

# Envie a mensagem "HELLO" para o cliente
message = "HELLO"
client_socket.send(message.encode())

# Fechar a conexão com o cliente
client_socket.close()

# Fechar o socket do servidor
server_socket.close()
