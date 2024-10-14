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

        http_response = f"HTTP/1.1 200 OK\n" \
                        f"Content-Type: text/html\n" \
                        f"Content-Length: {len(html_content)}\n\n" \
                        f"{html_content}"

        conn.sendall(http_response.encode())

    finally:
        conn.close()