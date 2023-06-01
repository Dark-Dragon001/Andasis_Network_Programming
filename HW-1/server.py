import socket
import threading
import time

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        super(ClientHandler, self).__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.running = True

    def run(self):
        while self.running:
            data = self.client_socket.recv(1024)
            if data:
                # Process received data
                # Apply rules and perform necessary actions
                print(f"Received data from {self.client_address}: {data.decode()}")

    def stop(self):
        self.running = False

def start_server():
    host = '127.0.0.1'
    port = 9000
    clients = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        client_handler = ClientHandler(client_socket, client_address)
        client_handler.start()
        clients.append(client_handler)


    # Clean up
    server_socket.close()
    for client in clients:
        client.stop()
        client.join()

start_server()
