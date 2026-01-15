import socket
import threading

HOST = "127.0.0.1"   # Localhost
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

print("🟢 Server started. Waiting for connections...")

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f"{name} left the chat.".encode("utf-8"))
            names.remove(name)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NAME".encode("utf-8"))
        name = client.recv(1024).decode("utf-8")

        names.append(name)
        clients.append(client)

        print(f"Name of the client is {name}")
        broadcast(f"{name} joined the chat!".encode("utf-8"))
        client.send("Connected to the server!".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
