import socket

# Defina o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substitua pelo IP do servidor
port = 10000  # Substitua pela porta usada pelo servidor

# Crie um socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
client_socket.connect((host, port))

# Receber uma resposta do servidor
response = client_socket.recv(1024)
# Imprimir a resposta recebida do servidor
print(f"Recebido do servidor: {response.decode()}")

# Enviar a mensagem "HELLO" de volta ao servidor
messagem = "HELLO"
client_socket.send(messagem.encode())



# Fechar a conexão com o servidor
client_socket.close()

