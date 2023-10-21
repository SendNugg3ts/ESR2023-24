import socket

# Defina o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substitua pelo IP do seu servidor
port = 3000  # Substitua pela porta usada pelo servidor

# Crie um socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecte-se ao servidor
client_socket.connect((host, port))

# Receba a mensagem "HELLO" do servidor
message = client_socket.recv(1024)

# Imprima a mensagem recebida
print(f"Recebido do servidor: {message.decode()}")

# Feche a conexão com o servidor
client_socket.close()
