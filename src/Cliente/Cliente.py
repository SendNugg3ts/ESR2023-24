import socket
from tkinter import Tk
from time import sleep
import os
from Cliente.ClientWorker import ClientWorker



def clientStartMessaging(host,port):
    # Criar um socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    
    message = "HELLO"
    client_socket.send(message.encode())

    response = client_socket.recv(1024)
    print(f"Recebido do servidor: {response.decode()}")

    client_socket.close()

def clientGuiStart(serverIP,serverPort, addr, port, name, filename):
    print(f'\nA iniciar {name} à escuta em {addr}:{port}')
    while True:
        
        if os.environ.get('DISPLAY', '') == '':
            print('Nenhum display encontrado, Usar DISPLAY :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        root = Tk()
        # Create a new client
        app = ClientWorker(root,serverIP,serverPort,addr,port,filename)
        app.master.title("RTP Client")
        root.wait_visibility()
        root.mainloop()
        sleep(2)
    