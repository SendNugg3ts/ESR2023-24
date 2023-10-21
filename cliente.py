import socket

# Defina o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substitua pelo IP do servidor
port = 10000  # Substitua pela porta usada pelo servidor

# Crie um socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecte-se ao servidor
client_socket.connect((host, port))

while True:
    # Envie uma mensagem para o servidor
    message = "Olá, servidor!"
    client_socket.send(message.encode())

    # Receba uma resposta do servidor
    response = client_socket.recv(1024)
    if not response:
        break  # Se não houver mais respostas do servidor, saia do loop

    # Imprimir a resposta recebida do servidor
    print(f"Recebido do servidor: {response.decode()}")

# Feche a conexão com o servidor
client_socket.close()
