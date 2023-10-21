import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('', 3000))

while True:
    mensagem_bytes,endereco_ip_cliente = servidor.recvfrom(2048)
    servidor.sendto("Hello".encode().endereco_ip_cliente)
