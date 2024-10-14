import socket
import threading

server_address = ('localhost', 9090)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen()

clients = []

def broadcast(message, exclude_client=None):
    for client in clients:
        if client != exclude_client:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client):
    nickname = client.recv(1024).decode()

    broadcast(f"{nickname} присоединился к чату.".encode(), exclude_client=client)
    clients.append(client)

    try:
        while True:
            message = client.recv(1024)
            if message:
                formatted_message = f"{nickname}: {message.decode()}"
                print(formatted_message)
                broadcast(formatted_message.encode(), exclude_client=client)
            else:
                break
    except:
        pass
    finally:
        broadcast(f"{nickname} покинул чат.".encode(), exclude_client=client)
        clients.remove(client)
        client.close()

def start_server():
    print("Сервер запущен и ожидает подключений...")
    while True:
        client, addr = sock.accept()
        print(f"Подключен клиент: {addr}")

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

start_server()