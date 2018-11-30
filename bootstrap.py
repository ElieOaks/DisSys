#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket as sock
from uuid import uuid4
from threading import Thread


#Function that starts a new thread for every new connection.
def accept_incoming_connections():
	"""Sets up handling for incoming clients."""
	while True:
		try:
			peer_socket, peer_address = SERVER.accept()
			print("%s:%s has connected." % peer_address)
			nick = get_nick(peer_socket)
			active_connections[peer_socket] = (nick, peer_address)
			peer_list[nick] = peer_address
			Thread(target=handle_peer, args=(peer_socket,)).start()
		except KeyboardInterrupt:
			return

def get_nick(peer_socket):
	while True:
		try:
			msg = peer_socket.recv(BUFSIZ)
			flag = msg[0:1].decode()
			content = msg[1:].decode()
			if flag == 'n':
				return content
			elif flag == 'g':
				peer_socket.sendall(b''+NICK)
			else:
				peer_socket.sendall(b'g')

# Handles the socket object of a peer
# Message flag table:
# u		Update me - Send me your list of peers
# p		Peer - Insert this peer into your list	
# g		Give nick - Send me your nick
def handle_peer(peer_socket):  # Takes client socket as argument.

	while True:
		# Decoding the message
		msg = peer_socket.recv(BUFSIZ)
		flag = msg.[0:1].decode()
		content = msg[1:].decode()

		# Peer wants to get list of addresses
		if flag == 'u':
			for peer in peer_list:
				print("Sending peer: %s" peer)
				peer_socket.send(b'i'+ bytes((peer, peer_list[peer])))
		
		# Accept incoming peer info
		if flag == 'p':
			print("Accepting peer %s" content)
			(nick, peer_address) = content
			peer_list[nick] = peer_address

		# Send back bootstrap nick
		if flag == 'g':
			print("Sending nick")
			peer_socket.sendall(b'n'+NICK)

		else:
			peer_socket.close()
			return
"""  
# Broadcast function
def broadcast(msg, prefix=""):  # prefix is for name identification.

	for sock in clients:
		sock.send(bytes(prefix+msg))
"""

active_connections = {}	
peer_list = {}

NICK = ''
HOST = ''
PORT = 33001
BUFSIZ = 1024
ADDR = (HOST, PORT)

if __name__ == "__main__":
	x = ''
	while len(x) != 1:
		x = raw_input("Are you a client? (y/n)")
	if x == 'n':
		initiate_bootstrap()
	else:
		initiate_client()

def initiate_client():
	NICK = raw_input("What is your nick?")

def initiate_bootstrap():
	NICK = 'bootstrap'
	SERVER = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
	SERVER.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
	SERVER.bind(ADDR)
	SERVER.listen(5)
	print("Waiting for connection...")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.daemon = True
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
