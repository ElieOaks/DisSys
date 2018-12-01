#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket as sock
from threading import Thread
import time
import sys


class Bootstrap:
	NICK = 'bootstrap'
	HOST = ''
	PORT = 33000
	BUFSIZ = 1024
	ADDR = (HOST, PORT)
	BOOTSTRAP = None

	active_connections = {}
	peer_list = {}

	def __init__(self):
		self.BOOTSTRAP = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		self.BOOTSTRAP.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		self.BOOTSTRAP.bind(self.ADDR)
		self.BOOTSTRAP.listen(5)
		print("Waiting for connection...")
		ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
		ACCEPT_THREAD.daemon = True
		ACCEPT_THREAD.start()
		ACCEPT_THREAD.join()
		self.BOOTSTRAP.close()

	#Function that starts a new thread for every new connection.
	def accept_incoming_connections(self):
		"""Sets up handling for incoming clients."""
		while True:
			try:
				peer_socket, peer_address = self.BOOTSTRAP.accept()
				print("%s:%s has connected." % peer_address)
				nick = self.get_nick(peer_socket)
				self.active_connections[peer_socket] = (nick, peer_address)
				self.peer_list[nick] = peer_address
				Thread(target=self.handle_peer, args=(peer_socket)).start()
			except KeyboardInterrupt:
				sys.exit(0)

	def get_nick(self, peer_socket):
		while True:
			try:
				msg = peer_socket.recv(self.BUFSIZ)
				flag = msg[0:1].decode()
				content = msg[1:].decode()

				if flag == 'n':
					return content
				elif flag == 'g':
					peer_socket.sendall(b''+self.NICK)
				else:
					peer_socket.sendall(b'g')
			except KeyboardInterrupt:
				sys.exit(0)
			except:
				return "Error"
		

	def handle_peer(self, peer_socket):
		while True:
			# Decoding the message
			msg = peer_socket.recv(self.BUFSIZ)
			flag = msg[0:1].decode()
			content = msg[1:].decode()
			# Peer wants to get list of addresses
			if flag == 'u':
				for peer in self.peer_list:
					print("Sending peer: %s" % peer)
					peer_socket.send(b'i'+ bytes((peer, self.peer_list[peer])))
			# Accept incoming peer info
			if flag == 'p':
				print("Accepting peer %s" % content)
				(nick, peer_address) = content
				self.peer_list[nick] = peer_address
			# Send back nick
			if flag == 'g':
				print("Sending nick")
				peer_socket.sendall(b'n'+self.NICK)
			else:
				peer_socket.close()
				return

class Client:
	NICK = 'bootstrap'
	HOST = ''
	PORT = 33000
	BUFSIZ = 1024
	ADDR = (HOST, PORT)

	active_connections = {}
	peer_list = {}

	def __init__(self):
		NICK = raw_input("What is your nick?")
		BOOTSTRAP_CONNECTION = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		BOOTSTRAP_CONNECTION.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		BOOTSTRAP_CONNECTION.connect(self.ADDR)
		print("Connected to bootstrap")
		BOOTSTRAP_THREAD = Thread(target=self.handle_peer, args=(BOOTSTRAP_CONNECTION,))
		BOOTSTRAP_THREAD.daemon = True
		BOOTSTRAP_THREAD.start()
		BOOTSTRAP_THREAD.join()
		BOOTSTRAP_CONNECTION.close()


	def handle_peer(self, peer_socket):
		while True:
			# Decoding the message
			msg = peer_socket.recv(self.BUFSIZ)
			flag = msg[0:1].decode()
			content = msg[1:].decode()
			# Peer wants to get list of addresses
			if flag == 'u':
				for peer in self.peer_list:
					print("Sending peer: %s" % peer)
					peer_socket.send(b'i'+ bytes((peer, self.peer_list[peer])))
			# Accept incoming peer info
			if flag == 'p':
				print("Accepting peer %s" % content)
				(nick, peer_address) = content
				self.peer_list[nick] = peer_address
			# Send back nick
			if flag == 'g':
				print("Sending nick")
				peer_socket.sendall(b'n'+self.NICK)
			else:
				peer_socket.close()
				return


if __name__ == "__main__":
	x = ''
	while len(x) != 1:
		x = raw_input("Are you a client? (y/n)")
	if x == 'y':
		Client()
	else:
		Bootstrap()

