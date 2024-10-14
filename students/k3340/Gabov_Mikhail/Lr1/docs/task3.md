# Задание 3: HTTP-сервер, возвращающий HTML-страницу

## Описание задания

В этом задании необходимо реализовать серверную часть приложения, которая возвращает клиенту HTML-страницу. Когда клиент подключается к серверу, он получает HTTP-ответ, содержащий HTML-страницу, загруженную с сервера из файла `index.html`.

## Требования

- Использовать библиотеку `socket`.
- Сервер должен отвечать клиенту с использованием протокола HTTP.

## Листинг кода

### HTML-страница (`index.html`):

```html
<!DOCTYPE html>
<html>
<head>
    <title>Simple HTTP Server</title>
</head>
<body>
    <h1>Welcome to the HTTP Server!</h1>
    <p>This is a simple HTML page.</p>
</body>
</html>
```

### Серверная часть (`server.py`):

```python
import socket

def load_html():
    with open('index.html', 'r') as file:
        return file.read()

server_address = ('localhost', 8080)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)

print("Сервер запущен: порт 8080")

while True:
    conn, addr = sock.accept()
    print(f"Подключен клиент: {addr}")

    try:
        request = conn.recv(1024).decode()
        print(f"Запрос клиента:\n{request}")

        html_content = load_html()

        http_response = f"HTTP/1.1 200 OK\n"                         f"Content-Type: text/html\n"                         f"Content-Length: {len(html_content)}\n\n"                         f"{html_content}"

        conn.sendall(http_response.encode())

    finally:
        conn.close()
```

## Описание выполнения

Сервер ожидает подключения клиента. Когда клиент подключается, сервер загружает HTML-страницу из файла `index.html` и отправляет её в качестве HTTP-ответа. Клиент видит HTML-страницу в своем браузере.