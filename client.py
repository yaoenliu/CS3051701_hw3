import socket
import sys
import threading

def start_client(host = "127.0.0.1", port = 12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("connected to the server.")

    # Start a thread to receive messages from the server
    thread = threading.Thread(target=receive_message,daemon = True, args=(client,))
    thread.start()   

    # Send messages to the server
    while True:
        message = input("")
        sys.stdout.write("\033[F\033[K")
        client.send(message.encode("utf-8"))
        if message == "exit":
            print("You left the chat. Disconnected from server.")
            break
        if message == "":
            sys.stdout.write(">> ")
        continue
    client.close()    
    return
    

def receive_message(client):
    while True:
        message = client.recv(1024).decode("utf-8")
        sys.stdout.write("\033[1K\033[1G")
        print(message)
        sys.stdout.write(">> ")
        sys.stdout.flush()

if __name__ == "__main__":
    start_client()