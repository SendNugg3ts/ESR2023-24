import socket

# Defina o endereço IP e a porta do servidor
host = '10.0.0.10'  # Substitua pelo IP do servidor
port = 10000  # Substitua pela porta usada pelo servidor

# Crie um socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
client_socket.connect((host, port))

while True:
    # Solicitar uma mensagem ao cliente
    message = input("Digite uma mensagem (ou 'fim' para encerrar): ")

    # Enviar a mensagem para o servidor
    client_socket.send(message.encode())

    # Verificar se o cliente deseja terminar a comunicação
    if message == "fim":
        break

    # Receber uma resposta do servidor
    response = client_socket.recv(1024)

    # Imprimir a resposta recebida do servidor
    print(f"Recebido do servidor: {response.decode()}")

# Fechar a conexão com o servidor
client_socket.close()

