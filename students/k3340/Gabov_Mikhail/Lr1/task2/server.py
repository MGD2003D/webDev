import socket
import math

def perform_operation(operation, params):
    if operation == "1":
        # теорема Пифагора
        a, b = map(float, params)
        return math.sqrt(a ** 2 + b ** 2)
    elif operation == "2":
        # квадратное уравнение
        a, b, c = map(float, params)
        discriminant = b ** 2 - 4 * a * c
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b - math.sqrt(discriminant)) / (2 * a)
            return f"x1 = {x1}, x2 = {x2}"
        elif discriminant == 0:
            x = -b / (2 * a)
            return f"x = {x}"
        else:
            return "Нет действительных решений"
    elif operation == "3":
        # площадь трапеции
        a, b, h = map(float, params)
        return ((a + b) / 2) * h
    elif operation == "4":
        # площадь параллелограмма
        a, h = map(float, params)
        return a * h
    else:
        return "Неверная операция"


server_address = ('localhost', 9090)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)

while True:
    conn, addr = sock.accept()

    try:
        data = conn.recv(1024).decode()
        if not data:
            break

        data = data.split(',')
        operation = data[0]
        params = data[1:]

        result = perform_operation(operation, params)

        conn.sendall(str(result).encode())

    finally:
        conn.close()