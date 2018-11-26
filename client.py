#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import socket as sock
from threading import Thread
import text_messages as mes

class Client:
    
    def __init__(self, identity, server_connection, my_IP):
        self.ID = identity
        self.connected = server_connection
        self.IP = my_IP
        self.text_thread = mes.text_messages([])
      
    def login(username, password):
        return 0

    #creates object text and adds it to the text_messages which is the current conversation
    def send_message(self, message, recipient):
        from_user = self.ID
        self.text_thread.add_message(message, from_user, recipient, 0)
        return 0

    #creates object text and adds it to the text_messages which is the current conversation
    def recieved_message(self, cipher_text, sender):
        message = cipher_text
        self.text_thread.add_message(message, sender, self.ID, 0)
        return 0

    def ping_server():
        return 0

    #prints out all the messages in terminal
    def show_messages(self):
        self.text_thread.show_messages()

    def ping_user():
        return 0

    #saves all the messages in a text file with the name of the user
    def save_state(self):      
        name = self.ID + ".txt"
        f= open(name,"w+")
        f.write("%s\n" % self.ID)
        f.write("%d\n" % self.connected)
        f.write("%s\n" % self.IP)
        self.text_thread.loggout(f)
        f.close()

    def loggout(self):
        self.save_state()

    #If this user has a txtx file on current device, will open that. Otherwise loggs in as a new user.
    def loggin(self, file_name):
        try:
            f = open(file_name, "r")
        except:
            self.new_user()
            return
        
        self.ID = f.readline().rstrip('\n')
        self.connected = int(f.readline().rstrip('\n'))
        self.IP = f.readline().rstrip('\n')        
        self.text_thread.loggin(f)
        f.close()

    #createsa new user, has some flaws. 
    def new_user(self):
        identity = raw_input()

        self.ID = identity
        self.connected = False
        self.IP = "000.000.000.000"
        self.text_thread = mes.text_messages([])
        self.save_state()
        
        
        
        
    def eventloop(incoming_event):
        return 0


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(str(msg))
        except OSError:  # Possibly client has left the chat.
            return
        except KeyboardInterrupt:
            return


def send():
    """Handles sending of messages."""
    person = raw_input()
    client_socket.sendall(b''+person)
    do = Client(None, None, None)
    do.loggin(person+".txt")

    while True:
        msg = raw_input("")
        client_socket.sendall(b''+msg)
        do.send_message(msg, "Karin")
        if (msg == 'p'):
            do.show_messages()
        if msg == "q":
            break

    do.loggout() 
    print("Thank you " + person + " for using Sexy People Talk, where all sexy people can talk!")
    return



#----Now comes the sockets part----
HOST = ''
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
send_thread.join()
receive_thread.join()
client_socket.close()