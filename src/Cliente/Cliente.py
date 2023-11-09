import socket
from tkinter import Tk
import time
from time import sleep
import os
from Cliente.ClientWorker import ClientWorker



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
        continue
    
