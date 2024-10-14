import socket
import urllib.parse

grades = {}

html_template_path = 'index.html'

server_address = ('localhost', 8080)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(5)

def handle_request(request):
    headers = request.split('\n')
    method, path, _ = headers[0].split()

    if method == 'GET':
        return generate_grades_list()

    elif method == 'POST':
        content_length = int([header for header in headers if 'Content-Length:' in header][0].split()[1])
        body = request.split('\r\n\r\n')[1][:content_length]

        params = urllib.parse.parse_qs(body)
        subject = urllib.parse.unquote(params['subject'][0])
        grade = urllib.parse.unquote(params['grade'][0])

        if not grade.isdigit() or not (1 <= int(grade) <= 5):
            return "HTTP/1.1 400 Bad Request\nContent-Type: text/html; charset=utf-8\n\n" \
                   "<html><body><h2>Ошибка: Оценка должна быть числом от 1 до 5.</h2>" \
                   "<a href='/'>Назад к списку оценок</a></body></html>"

        grades[subject] = grade

        return "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" \
               "<html><body><h2>Оценка добавлена!</h2><a href='/'>Назад к списку оценок</a></body></html>"

def generate_grades_list():
    with open(html_template_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    grades_list = ''.join(f"<li>{subject}: {grade}</li>" for subject, grade in grades.items())

    html_content = html_content.replace('{{grades_list}}', grades_list)

    return "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" + html_content

def start_server():
    print(f"Сервер запущен на {server_address[0]}:{server_address[1]}")
    while True:
        client, addr = sock.accept()
        request = client.recv(1024).decode()
        if request:
            response = handle_request(request)
            client.sendall(response.encode('utf-8'))
        client.close()

start_server()