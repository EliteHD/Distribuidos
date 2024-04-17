import socket
import sys

def send_message(host, port, message):
    """Función para enviar mensajes a otro nodo o al servidor de registro."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
    return response

def register_with_server(server_host, server_port, my_host, my_port):
    """Función para registrar este nodo en el servidor de registro."""
    response = send_message(server_host, server_port, f"register {my_host} {my_port}")
    my_id = int(response.split()[1])
    print(f"I am registered with ID {my_id}")
    return my_id

def get_node_list(server_host, server_port):
    """Función para obtener la lista de nodos activos desde el servidor de registro."""
    nodes_info = send_message(server_host, server_port, "get nodes")
    nodes = []
    if nodes_info:
        entries = nodes_info.split(' ')
        for i in range(0, len(entries), 3):
            nodes.append({'id': int(entries[i]), 'host': entries[i+1], 'port': int(entries[i+2])})
    return nodes

def main(server_host, server_port, my_host, my_port):
    """Función principal para ejecutar el nodo cliente."""
    my_id = register_with_server(server_host, server_port, my_host, my_port)
    nodes = get_node_list(server_host, server_port)
    print("Current nodes:", nodes)
    # Desde aquí se pueden iniciar procesos adicionales, como el algoritmo de elección.

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 client.py [local_port] [my_host_ip]")
        sys.exit(1)
    my_port = int(sys.argv[1])
    my_host = sys.argv[2]
    # Configura la dirección IP del servidor y el puerto.
    server_host = '175.1.54.224'
    server_port = 5000
    main(server_host, server_port, my_host, my_port)
