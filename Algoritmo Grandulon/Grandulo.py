import socket
import threading
import random
import time

# Función para enviar mensajes a todos los nodos
def enviar_mensaje_a_todos(mensaje, puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for i in range(1, 255):
            direccion = f" 175.1.46.{i}"  # Cambia esto por la red que estés utilizando
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
            if recibido_identificador > identificador:
                gran_jefe[0] = recibido_identificador
                identificador = recibido_identificador
                print(f"Nodo con identificador {identificador} es el nuevo gran jefe.")
            else:
                print(f"Nodo con identificador {recibido_identificador} intentó ser el gran jefe, pero no superó a {identificador}.")

# Función para obtener un identificador aleatorio
def obtener_identificador():
    return random.randint(1, 1000)

# Función principal
def main():
    identificador = obtener_identificador()
    puerto = 5000
    gran_jefe = [identificador]

    print(f"El identificador de este nodo es: {identificador}")

    # Iniciar hilo para escuchar mensajes
    thread_escucha = threading.Thread(target=escuchar_mensajes, args=(puerto, identificador, gran_jefe))
    thread_escucha.start()

    # Enviar mensaje a todos los nodos
    mensaje = f"{identificador}:¡Soy el gran jefe!"
    enviar_mensaje_a_todos(mensaje, puerto)

    # Ciclo para simular desconexiones y nuevas elecciones de gran jefe
    while True:
        time.sleep(10)  # Espera 10 segundos antes de simular una desconexión y una nueva elección del gran jefe

        # Simular desconexión del gran jefe
        print(f"El nodo con identificador {gran_jefe[0]} se ha desconectado.")
        gran_jefe[0] = obtener_identificador()
        print(f"El nuevo gran jefe será el nodo con identificador {gran_jefe[0]}.")

        # Reiniciar proceso de elección de gran jefe
        mensaje = f"{gran_jefe[0]}:¡Soy el gran jefe!"
        enviar_mensaje_a_todos(mensaje, puerto)

if __name__ == "__main__":
    main()
