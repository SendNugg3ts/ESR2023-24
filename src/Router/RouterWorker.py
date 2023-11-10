import socket
import threading

class RoutersWorker:
    def __init__(self, rp_address, rp_port, neighbors):
        self.rp_address = rp_address
        self.rp_port = rp_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', 0))  # Bind to any available interface and port
        self.server_address = self.server_socket.getsockname()
        self.clients = set()
        self.neighbors = neighbors  # List of neighbors: [client1, client2, other_router, RP]

    def run(self):
        # Start listening for requests from clients
        threading.Thread(target=self.listen_for_requests).start()

    def listen_for_requests(self):
        while True:
            data, client_address = self.server_socket.recvfrom(1024)
            message = data.decode()

            # Assuming the message format is "REQUEST:video_id"
            if message.startswith("REQUEST:"):
                video_id = message[len("REQUEST:"):]
                self.forward_video_request(video_id, client_address)

    def forward_video_request(self, video_id, client_address):
        # Try to forward the request to neighbors
        if self.forward_request_to_neighbors(video_id, client_address):
            return

        # If no neighbor has the video, forward the request to the RP
        rp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rp_socket.sendto(f"REQUEST:{video_id}".encode(), (self.rp_address, self.rp_port))
        rp_socket.close()

        # Add the client to the set of clients
        self.clients.add(client_address)

    def forward_request_to_neighbors(self, video_id, client_address):
        # Try to forward the request to neighbors
        for neighbor_address in self.neighbors:
            neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                neighbor_socket.sendto(f"REQUEST:{video_id}".encode(), neighbor_address)
                neighbor_socket.close()
                return True  # Successfully forwarded the request to a neighbor
            except socket.error:
                # Error handling if the neighbor is not reachable
                neighbor_socket.close()
                continue

        return False  # No neighbor had the video

    def forward_video_to_clients(self, video_data):
        # Forward video data to all clients
        for client_address in self.clients:
            self.server_socket.sendto(video_data, client_address)

    def close(self):
        self.server_socket.close()

