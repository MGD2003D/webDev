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