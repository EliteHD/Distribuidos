import socket
import sys
import threading

def send_message(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
    return response

def register_with_server(server_host, server_port, my_host, my_port):
    response = send_message(server_host, server_port, f"register {my_host} {my_port}")
    my_id = int(response.split()[1])
    print(f"I am registered with ID {my_id}")
    return my_id

def get_node_list(server_host, server_port):
    nodes_info = send_message(server_host, server_port, "get nodes")
    nodes = []
    if nodes_info:
        entries = nodes_info.split(' ')
        for i in range(0, len(entries), 3):
            nodes.append({'id': int(entries[i]), 'host': entries[i+1], 'port': int(entries[i+2])})
    return nodes

def main(server_host, server_port, my_host, my_port):
    my_id = register_with_server(server_host, server_port, my_host, my_port)
    nodes = get_node_list(server_host, server_port)
    print("Current nodes:", nodes)
    # Aquí podrías iniciar el proceso de elección u otras operaciones

if __name__ == '__main__':
    # Asegúrate de cambiar aquí el puerto a uno apropiado que esté libre en tu máquina
    main('175.1.54.224', 5000, 'localhost', int(sys.argv[1]))
