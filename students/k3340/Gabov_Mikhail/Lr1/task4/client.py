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