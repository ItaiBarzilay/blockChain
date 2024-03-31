import socket
import threading

# Function to handle incoming messages from the server
def receive_messages(client_socket):
    while True:
        try:
            # Receive message from server
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(data)

        except Exception as e:
            print("Exception in receive_messages:", e)
            break

# Function to start the client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    print("Connected to server.")

    # Start thread to receive messages from server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Send messages to the server
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

# Start the client
start_client()
