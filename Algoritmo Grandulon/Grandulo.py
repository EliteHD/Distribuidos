import socket
import threading

# Función para enviar mensajes a todos los nodos
def enviar_mensaje_a_todos(mensaje, puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for i in range(1, 255):
            direccion = f"175.1.{i}.{i}"  # Cambia esto por la red que estés utilizando
            try:
                sock.sendto(mensaje.encode(), (direccion, puerto))
            except OSError:
                pass

# Función que escucha mensajes y determina al "gran jefe"
def escuchar_mensajes(puerto, identificador, gran_jefe):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("0.0.0.0", puerto))
        while True:
            mensaje, direccion = sock.recvfrom(1024)
            mensaje = mensaje.decode()
            recibido_identificador = int(mensaje.split(":")[0])
            if recibido_identificador > gran_jefe[0]:
                gran_jefe[0] = recibido_identificador
                print(f"Nodo con identificador {gran_jefe[0]} es el nuevo gran jefe.")

# Función para obtener el identificador basado en la dirección IP
def obtener_identificador():
    direccion_ip = socket.gethostbyname(socket.gethostname())
    partes_ip = direccion_ip.split('.')
    identificador = int(partes_ip[-1])  # Tomar el último octeto de la dirección IP
    return identificador

# Función principal
def main():
    identificador = obtener_identificador()
    puerto = 5000
    gran_jefe = [identificador]

    # Iniciar hilo para escuchar mensajes
    thread_escucha = threading.Thread(target=escuchar_mensajes, args=(puerto, identificador, gran_jefe))
    thread_escucha.start()

    # Enviar mensaje a todos los nodos
    mensaje = f"{identificador}:¡Soy el gran jefe!"
    enviar_mensaje_a_todos(mensaje, puerto)

    # Esperar a que se elija al gran jefe
    thread_escucha.join()

if __name__ == "__main__":
    main()
