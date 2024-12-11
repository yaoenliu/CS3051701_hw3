import socket
import threading
from dataclasses import dataclass

@dataclass
class Client:
    """ Dataclass to store client information 
    Args:
        socket (socket.socket): The client's socket
        name (str): The client's name
    """
    socket : socket.socket
    name : str


ClientList: list[Client] = [] 
""" List of connected clients """


def broadcast(message: str):
    """ 
    Broadcasts a message to all connected clients 
    Args:
        message (str): The message to be broadcasted
    """
    for client in ClientList:
        client.socket.send(message.encode("utf-8"))
    return

def start_server(host = "127.0.0.1", port = 12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
    return

def handle_client(client_socket):

    Pass = False
    
    while not Pass:
        Pass = True
        client_socket.send("Enter your name: ".encode("utf-8"))
        try:
            name = client_socket.recv(1024).decode("utf-8")
        except:
            # 有人在输入名字的時候關掉視窗
            print (f"A disconnection from {client_socket.getpeername()} before entering a name.")
            return
        if len(ClientList) == 5:
            client_socket.send("Unable to connect server: Maximum connections reached.".encode("utf-8"))
            print(f"Connection attempt from ({client_socket.getpeername()}) rejected: Maximum connections reached.")
            Pass = False
            continue
        for client in ClientList:
            if client.name == name:
                Pass = False
                client_socket.send("Name already in use. Please enter a different name.".encode("utf-8"))
                break
    
    ClientList.append(Client(client_socket, name)) 
    broadcast(f"{name} has joined the chat.")    
    print(f"{name} has joined the chat.")

    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data or data == "exit":            
                break
            print (f"{name} sent: {data}")
            broadcast(f"{name}: {data}")
        except:
            # 有人在聊天的時候關掉視窗            
            break
        
    ClientList.remove(Client(client_socket, name))
    broadcast(f"{name} has left the chat.")
    print(f"{name} has left the chat.")
    client_socket.close()

if __name__ == "__main__":
    start_server()

