import socket
import threading
import datetime
import json
from blockchain import Block, Blockchain

# Initialize the blockchain
blockchain = Blockchain()

# Function to handle incoming messages
def handle_client(client_socket, address):
    while True:
        try:
            # Receive message from client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Add message to blockchain
            new_block = Block(len(blockchain.chain), datetime.datetime.now(), {"sender": str(address), "message": data}, blockchain.get_latest_block().hash)
            blockchain.add_block(new_block)
            print("New message added to blockchain.")

            # Broadcast message to other clients
            for client in clients:
                if client != client_socket:
                    client.send(data.encode('utf-8'))

        except Exception as e:
            print("Exception in handle_client:", e)
            break

    # Remove client from list
    clients.remove(client_socket)
    client_socket.close()

# Function to start the chat server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server started. Waiting for connections...")

    while True:
        client_socket, address = server.accept()
        print("Connection from:", address)
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

# Function to display the chat history stored in the blockchain
def display_chat_history():
    print("\nChat History:")
    for block in blockchain.chain:
        print(f"Block {block.index}: {str(block.data)}")

# List to keep track of connected clients
clients = []

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Allow the server to run while providing an option to view chat history
while True:
    command = input("\nEnter 'history' to view chat history or 'exit' to stop the server: ")
    if command.lower() == 'history':
        display_chat_history()
    elif command.lower() == 'exit':
        break
    else:
        print("Invalid command. Please try again.")

# Close the server socket
print("Stopping server...")
server_thread.join()
