#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import socket as sock
from threading import Thread
try:
    import tkinter
except ImportError:
    import Tkinter

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(str(msg))
            #msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break
        except KeyboardInterrupt:
            exit()


def send():
    """Handles sending of messages."""
    while True:
        msg = input("Your message: ")
        #msg = my_msg.get()
        #my_msg.set("")  # Clears input field.
        client_socket.sendall(b""+msg)
        if msg == "q":
            client_socket.close()
            #top.quit()

"""  
def on_closing(event=None):
    #This function is to be called when the window is closed.
    my_msg.set("{quit}")
    send()
"""


""" 
top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
"""

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