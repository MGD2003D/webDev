
# Задание 1: UDP-сервер и клиент

## Описание задания

В этом задании необходимо реализовать клиентскую и серверную часть приложения, используя протокол UDP. Клиент отправляет серверу сообщение "Hello, server!", которое отображается на стороне сервера. В ответ сервер отправляет клиенту сообщение "Hello, client!", и оно должно отобразиться на стороне клиента.

## Требования

- Использовать библиотеку `socket`.
- Реализовать с помощью протокола UDP.

## Листинг кода

### Клиентская часть (`client.py`):

```python
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
```

### Серверная часть (`server.py`):

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 9090))

while True:
    data, addr = sock.recvfrom(1024)
    print(data.decode())

    rsp = "Hello, client!"
    sock.sendto(rsp.encode(), addr)
```