import socket
import threading
import time
import sys

class Node:
    def __init__(self, node_id, ip, port, peers):
        self.node_id = node_id
        self.ip = ip
        self.port = port
        self.peers = peers  # Diccionario de peers donde las claves son los IDs y los valores son tuplas de (IP, puerto)
        self.coordinator = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(10)
        print(f"Node {self.node_id} listening on {ip}:{port}")

    def handle_connection(self, conn, addr):
        while True:
            try:
                message = conn.recv(1024).decode()
                if message:
                    print(f"Node {self.node_id} received message: {message} from {addr}")
                    cmd, src_id = message.split(',')
                    if cmd == 'ELECTION':
                        self.respond_to_election(int(src_id))
                    elif cmd == 'COORDINATOR':
                        self.coordinator = int(src_id)
                        print(f"Node {self.node_id}: New coordinator is {self.coordinator}")
            except:
                break

    def respond_to_election(self, src_id):
        if self.node_id > src_id:
            self.send_message(src_id, 'RESPONSE')
            self.start_election()

    def start_election(self):
        responses = False
        for pid, (p_ip, p_port) in self.peers.items():
            if pid > self.node_id:
                if self.send_message(pid, 'ELECTION'):
                    responses = True
        if not responses:
            self.announce_coordinator()

    def announce_coordinator(self):
        self.coordinator = self.node_id
        for pid, (p_ip, p_port) in self.peers.items():
            self.send_message(pid, 'COORDINATOR')

    def send_message(self, peer_id, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.peers[peer_id][0], self.peers[peer_id][1]))
                sock.send(f"{message},{self.node_id}".encode())
                return True
        except:
            return False

    def listen(self):
        while True:
            conn, addr = self.socket.accept()
            threading.Thread(target=self.handle_connection, args=(conn, addr)).start()

    def close(self):
        self.socket.close()

if __name__ == '__main__':
    node_id = int(sys.argv[1])
    ip = sys.argv[2]
    port = int(sys.argv[3])
    peers = {1: ('175.1.54.224', 5000), 2: ('175.1.54.224', 5001), 3: ('175.1.54.224', 5002)}

    node = Node(node_id, ip, port, peers)
    try:
        threading.Thread(target=node.listen).start()
    except Exception as e:
        print(f"Error: {e}")
        node.close()
