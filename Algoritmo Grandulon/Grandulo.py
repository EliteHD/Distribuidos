
import socket
import threading
import time
import sys
import json

class Node:
    def __init__(self, identifier, host, port, nodes_info):
        self.identifier = identifier
        self.host = host
        self.port = port
        self.nodes_info = nodes_info  # Dictionary of other nodes' IDs, hosts, and ports
        self.leader = None
        self.running = True
        self.lock = threading.Lock()

    def start_node(self):
        threading.Thread(target=self.run_server).start()

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f'Node {self.identifier} listening on {self.host}:{self.port}')
            while self.running:
                conn, addr = server_socket.accept()
                threading.Thread(target=self.handle_connection, args=(conn,)).start()

    def handle_connection(self, conn):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                self.process_message(message, conn)

    def process_message(self, message, conn):
        if message.startswith('ELECTION'):
            self.respond_to_election(message, conn)
        elif message.startswith('COORDINATOR'):
            self.acknowledge_leader(message)

    def respond_to_election(self, message, conn):
        sender_id = int(message.split()[-1])
        if self.identifier > sender_id:
            conn.sendall(f'OK {self.identifier}'.encode())

    def acknowledge_leader(self, message):
        leader_id = int(message.split()[-1])
        with self.lock:
            self.leader = leader_id
            print(f'Node {self.identifier}: Acknowledged new leader {self.leader}')

    def initiate_election(self):
        higher_nodes = [(id_, info) for id_, info in self.nodes_info.items() if id_ > self.identifier]
        responses = []
        for node_id, (host, port) in higher_nodes:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((host, port))
                    client_socket.sendall(f'ELECTION {self.identifier}'.encode())
                    response = client_socket.recv(1024).decode()
                    if response.startswith('OK'):
                        responses.append(node_id)
            except (ConnectionRefusedError, socket.timeout):
                continue

        if not responses:  # No higher node responded
            self.declare_as_leader()
        else:
            print(f'Node {self.identifier} received OK from {responses}')

    def declare_as_leader(self):
        self.leader = self.identifier
        print(f'Node {self.identifier} declares itself as the leader')
        for node_id, (host, port) in self.nodes_info.items():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((host, port))
                    client_socket.sendall(f'COORDINATOR {self.identifier}'.encode())
            except ConnectionRefusedError:
                continue

    def stop_node(self):
        self.running = False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 node.py <config_file> <node_id>")
        sys.exit(1)
    
    config_file, node_id = sys.argv[1], int(sys.argv[2])
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    nodes_info = {int(id_): tuple(info) for id_, info in config['nodes'].items()}
    host, port = nodes_info[node_id]

    node = Node(node_id, host, port, nodes_info)
    node.start_node()
    time.sleep(2)  # Allow nodes to start up
    if node_id == min(nodes_info.keys()):  # Let the smallest ID node start an election
        node.initiate_election()
