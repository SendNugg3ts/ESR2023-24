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

# Receber uma resposta do cliente
response = client_socket.recv(1024)
# Imprimir a resposta recebida do cliente
print(f"Recebido do cliente: {response.decode()}")

# Enviar a mensagem "HELLO" de volta ao cliente
message = "HELLO"
client_socket.send(message.encode())

# Fechar a conexão com o cliente
client_socket.close()

# Fechar o socket do servidor
server_socket.close()


