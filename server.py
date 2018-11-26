#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket as sock
from threading import Thread


#Function that starts a new thread for every new connection.
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        try:
                client, client_address = SERVER.accept()
                print("%s:%s has connected." % client_address)
                client.send(bytes("Welcome to the Sexy Peple Talk, input your name:"))
                addresses[client] = client_address
                Thread(target=handle_client, args=(client,)).start()
        except KeyboardInterrupt:
                return
#Individual function that handles a connection. First takes the nick of client and broadcasts all messages.
def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit (unlikely), type q to exit.' % name
    client.send(bytes(welcome   ))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("q"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("q"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name))
            return

# Broadscast function
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix+msg))

        
clients = {}
addresses = {}

HOST = ''
PORT = 33001
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
SERVER.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
SERVER.bind(ADDR)
SERVER.listen(5)
print(sock.gethostbyname(sock.gethostname()))
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=accept_incoming_connections)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()
