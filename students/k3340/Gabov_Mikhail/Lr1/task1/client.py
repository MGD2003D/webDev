import socket

server_address = ('localhost', 9090)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    message = "Hello, server!"
    print(message)
    sock.sendto(message.encode(), server_address)

    data, server = sock.recvfrom(1024)
    print(data.decode())

finally:
    sock.close()