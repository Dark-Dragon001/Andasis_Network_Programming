import socket
import random
import time

def start_client():
    host = '127.0.0.1'
    port = 9000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server")

    while True:
        # Generate temperature data
        temperature = random.uniform(10, 50)

        # Send temperature data to server
        client_socket.sendall(str(temperature).encode())

        # Sleep for a specified interval
        time.sleep(1)  # Adjust this according to the desired data transmission frequency


    # Clean up
    client_socket.close()

start_client()
