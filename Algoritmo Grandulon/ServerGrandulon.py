import socket
import threading
import json

def client_thread(conn, addr, nodes):
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        if data.startswith('register'):
            node_id = len(nodes) + 1
            nodes[node_id] = addr
            conn.sendall(json.dumps({'id': node_id, 'nodes': nodes}).encode('utf-8'))
        elif data.startswith('update'):
            conn.sendall(json.dumps({'nodes': nodes}).encode('utf-8'))
    conn.close()

def main():
    host = '175.1.54.224'
    port = 5000
    nodes = {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Servidor de registro corriendo...")
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=client_thread, args=(conn, addr, nodes)).start()

if __name__ == '__main__':
    main()
