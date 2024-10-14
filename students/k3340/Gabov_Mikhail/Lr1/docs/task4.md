# Задание 4: Многопользовательский чат

## Описание задания

Необходимо реализовать многопользовательский чат с использованием протокола TCP. Клиенты подключаются к серверу, могут отправлять и получать сообщения в чате

## Требования

- Использовать библиотеку `socket`.
- Использовать библиотеку `threading` для многопользовательского чата.
- Реализовать через протокол TCP.

## Листинг кода

### Клиентская часть (`client.py`):

```python
import socket
import threading

nickname = input("Введите свой никнейм: ")

server_address = ("localhost", 9090)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)

sock.send(nickname.encode())

def receive_messages():
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Вы отключены от сервера.")
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input("")

    if message.lower() == 'exit':
        sock.send(f"{nickname} покинул чат.".encode())
        sock.close()
        break

    if message:
        sock.send(message.encode())
```

### Серверная часть (`server.py`):

```python
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
```

## Описание выполнения

- Клиенты вводят свой никнейм при подключении к серверу.
- Когда клиент отправляет сообщение, оно передается всем подключенным пользователям (кроме отправителя).
- Клиент может выйти из чата, отправив команду `exit`.
- Сервер поддерживает многопользовательский чат, обрабатывая каждого клиента в отдельном потоке.