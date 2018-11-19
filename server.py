import socket
import threading

#AF_INET = IPv4, SOCK_STREAM = TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to an IP address and port
sock.bind(('0.0.0.0', 10000))

#Defina max nr of connections
sock.listen(1)

connections = []

def handler(c, a):
    global connections
    while True:
        data = c.recv(1024)
        for connection in connections:
            connection.send(bytes(data))
        if not data:
            connections.remove(c)
            c.close
            break


while True:
    # C = connection, A = connection address
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c,a))

    # Allows program to exit even when there's active threads
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    print(connections)

