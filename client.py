#!/usr/bin/env python3
import socket as sock
from threading import Thread


def bootstrap_receive():
    """Handles communication """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ)
            
            #Updating peer list
            if(msg[0:1] == b'i'):
                print("Adding address %s to peer list" %msg[1:].decode)
        
            else:
                print(msg.decode("utf-8"))

        except OSError:  # Possibly client has left the chat.
            return
        except KeyboardInterrupt:
            return


def send():
    """Handles sending of messages."""
    person = raw_input()
    client_socket.sendall(b''+person)

    while True:
        msg = raw_input("")
        client_socket.sendall(b''+msg)
        do.send_message(msg, "Karin")
        if (msg == 'p'):
            do.show_messages()
        if msg == "q":
            break

    do.loggout() 
    #print("Thank you " + person + " for using Sexy People Talk, where all sexy people can talk!")
    return



#----Now comes the sockets part----
HOST = ''
PORT = 33001
PEERS = {}
NICK = raw_input("What is your nick?")

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
client_socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
client_socket.connect(ADDR)

bootstrap_thread = Thread(target=bootstrap_receive)
send_thread = Thread(target=send)
send_thread.start()
bootstrap_thread.start()
send_thread.join()
bootstrap_thread.join()
client_socket.close()