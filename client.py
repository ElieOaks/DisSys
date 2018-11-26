#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import socket as sock
from threading import Thread

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(str(msg))
        except OSError:  # Possibly client has left the chat.
            break
        except KeyboardInterrupt:
            exit()


def send():
    """Handles sending of messages."""
    while True:
        msg = raw_input("")
        client_socket.sendall(b''+msg)
        if msg == "q":
            exit()



#----Now comes the sockets part----
HOST = '127.0.0.1'
PORT = 33001

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
client_socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
send_thread.start()
receive_thread.start()
receive_thread.join()
send_thread.join()
client_socket.close()