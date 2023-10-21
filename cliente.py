import socket
# Definir o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substituir pelo IP do servidor
port = 10000  

# Criar um socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
client_socket.connect((host, port))

# Receber a mensagem "HELLO" do servidor
message = client_socket.recv(1024)

# Imprimir a mensagem recebida
print(f"Recebido do servidor: {message.decode()}")

# Feche a conexão com o servidor
client_socket.close()
