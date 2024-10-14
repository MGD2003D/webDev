# Задание 2: TCP-сервер и клиент для выполнения математических операций

## Описание задания

В этом задании клиент отправляет серверу запрос на выполнение математической операции (например, теорема Пифагора, решение квадратного уравнения), и сервер возвращает результат.

## Требования

- Использовать библиотеку `socket`.
- Реализовать с помощью протокола TCP.

## Варианты операций

1. Теорема Пифагора.
2. Решение квадратного уравнения.
3. Поиск площади трапеции.
4. Поиск площади параллелограмма.

## Листинг кода

### Клиентская часть (`client.py`):

```python
import socket

def input_operation():
    print("Выберите операцию:")
    print("1 - Теорема Пифагора")
    print("2 - Решение квадратного уравнения")
    print("3 - Площадь трапеции")
    print("4 - Площадь параллелограмма")
    operation = input("Введите номер операции: ")

    if operation == "1":
        a = input("Введите значение a: ")
        b = input("Введите значение b: ")
        return f"{operation},{a},{b}"
    elif operation == "2":
        a = input("Введите значение a: ")
        b = input("Введите значение b: ")
        c = input("Введите значение c: ")
        return f"{operation},{a},{b},{c}"
    elif operation == "3":
        a = input("Введите значение a (верхнее основание): ")
        b = input("Введите значение b (нижнее основание): ")
        h = input("Введите высоту h: ")
        return f"{operation},{a},{b},{h}"
    elif operation == "4":
        a = input("Введите значение a (основание): ")
        h = input("Введите высоту h: ")
        return f"{operation},{a},{h}"
    else:
        print("Неверная операция")
        return None

server_address = ('localhost', 9090)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)

try:
    data = input_operation()

    if data:
        sock.sendall(data.encode())
        result = sock.recv(1024).decode()
        print(f"Результат: {result}")
finally:
    sock.close()
```

### Серверная часть (`server.py`):

```python
import socket
import math

def perform_operation(operation, params):
    if operation == "1":
        a, b = map(float, params)
        return math.sqrt(a ** 2 + b ** 2)
    elif operation == "2":
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
        a, b, h = map(float, params)
        return ((a + b) / 2) * h
    elif operation == "4":
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
```

## Описание выполнения

Клиент выбирает операцию и отправляет параметры на сервер. Сервер обрабатывает запрос, вычисляет результат (например, решение теоремы Пифагора или уравнения) и отправляет его обратно клиенту.