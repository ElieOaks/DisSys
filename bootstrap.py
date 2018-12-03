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
	INC_PORT = 33001
	BUFSIZ = 1024
	ADDR = (HOST, PORT)
	#BOOTSTRAP = None

	peer_list = {}

	def __init__(self):
		# Setup bootstrap socket and wait for connections
		BOOTSTRAP = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		BOOTSTRAP.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		BOOTSTRAP.bind(self.ADDR)
		BOOTSTRAP.listen(5)
		print("Waiting for connection...")

		# Start the thread which listens for connections
		ACCEPT_THREAD = Thread(target=self.accept_incoming_connections_bootstrap, args=(BOOTSTRAP,))
		ACCEPT_THREAD.daemon = True
		ACCEPT_THREAD.start()
		ACCEPT_THREAD.join()

	#Function that starts a new thread for every new connection.
	def accept_incoming_connections_bootstrap(self, bootstrap_socket):
		"""Sets up handling for incoming clients."""
		while True:
			try:
				# Accepts incoming connection and adds it to peer list
				peer_socket, peer_address = bootstrap_socket.accept()
				nick = self.get_nick(peer_socket)
				print("%s:%s has connected." % peer_address)
				print("Nick: %s" % nick)
				self.peer_list[nick] = (peer_address, peer_socket)
				# Starts a handler for new peer
				Thread(target=self.handle_peer_bootstrap, args=(nick,)).start()
			except KeyboardInterrupt:
				return

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
				peer_socket.close()
				return
			except:
				return "Error"
		

	def handle_peer_bootstrap(self, nick):
		#Retreive the socket object via nick
		peer_socket = self.get_socket(nick)
		while True:
			try:
				# Decoding the message
				message = peer_socket.recv(self.BUFSIZ)
				flag = message[:1].decode()
				content = message[1:].decode()

				if flag == 'u':	
					for peer in self.peer_list:
						print("Sending peer: %s" % peer)
						peer_socket.send(bytes(('p' + bytes((nick, self.get_ip(peer))))))
				# Accept incoming peer info
				if flag == 'p':
					peers = self.split_peers(message)
					for peer in peers:
						print("Accepting peer %s" % peer)
						(inc_nick, ip) = eval(content)
						self.peer_list[inc_nick] = (ip, None)
				# Send back nick
				if flag == 'g':
					print("Sending nick")
					peer_socket.sendall(b'n'+self.NICK)
				else:
					peer_socket.close()
					return
			except KeyboardInterrupt:
				return

	def split_peers(self, messages):
		payload = [messages.split('p(')]
		for peer in payload:
			peer.prepend('(')
		return payload

	def get_socket(self, nick):
		(_, socket) = self.peer_list[nick]
		return socket

	def get_ip(self, nick):
		(ip, _) = self.peer_list[nick]
		(adr, _) = ip
		return adr




if __name__ == "__main__":
	Bootstrap()
