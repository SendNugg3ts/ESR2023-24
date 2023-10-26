import os
import re
from tkinter import Tk
from time import sleep
from ClienteStreamer import Client

def start_client(node_id, my_port, lock, message):
    """
    Start the RTP client based on the nearest server information.
    Args:
        node_id (str): The node ID.
        my_port (int): The client's port.
        lock (threading.Lock): A lock to ensure proper synchronization.
        message (dict): The message with server information.
    """
    print(f'\nStarting client listening on {node_id}:{my_port}')

    while not message['nearest_server']:
        sleep(1)

    while True:
        if not os.environ.get('DISPLAY', ''):
            print('No display found... Using DISPLAY :0.0')
            os.environ['DISPLAY'] = ':0.0'

        filename = "movie.Mjpeg"
        root = Tk()

        lock.acquire()
        print("nearest_server: " + str(message['nearest_server']))

        if message['nearest_server']:
            server_info = message['nearest_server'][0]
            server_addr, server_port = server_info[0], int(server_info[1])
            rtp_address, rtp_port = (node_id, my_port)
            lock.release()

            # Create a new client
            app = Client(root, server_addr, server_port, rtp_address, rtp_port, filename, server_info)
            app.master.title("RTP Client")
            root.wait_visibility()
            root.mainloop()
            sleep(2)

