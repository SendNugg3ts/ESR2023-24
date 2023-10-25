import socket

# Definir o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substituir pelo IP do servidor
port = 10000  # Substituir pela porta usada pelo servidor

# Criar um socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
client_socket.connect((host, port))

# Enviar a mensagem "HELLO" para o servidor
message = "HELLO"
client_socket.send(message.encode())

# Receber uma resposta do servidor
response = client_socket.recv(1024)
# Imprimir a resposta recebida do servidor
print(f"Recebido do servidor: {response.decode()}")

# Fechar a conexão com o servidor
client_socket.close()
