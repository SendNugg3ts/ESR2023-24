import socket
cliente= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    mensagem_envio= print("HELLO")
    cliente.sendto(mensagem_envio.encode("10.0.0.10"),3000)
    mensagem_bytes, endereco_ip_servidor= cliente.recvfrom(2048)
    print(mensagem_bytes.decode())

