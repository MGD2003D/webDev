import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 9090))

while True:
    data, addr = sock.recvfrom(1024)

    print(data.decode())

    rsp = "Hello, client!"
    sock.sendto(rsp.encode(), addr)