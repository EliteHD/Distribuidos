import socket
import json

def register_with_server(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        s.sendall('register'.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        return json.loads(data)

def main():
    server_ip = '175.1.54.224'
    server_port = 5000

    node_info = register_with_server(server_ip, server_port)
    my_id = node_info['id']
    nodes = node_info['nodes']

    print(f"Registered as Node {my_id} with nodes: {nodes}")

if __name__ == '__main__':
    main()
