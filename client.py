#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket as sock
from threading import Thread
import time as t
import sys

class Client:
	NICK = ''
	HOST = ''
	B_PORT = 33000
	INC_PORT = 33001
	BUFSIZ = 1024
	ADDR = (HOST, B_PORT)

	# Dictionary with nick as key, references IP and socket (if no connection established, socket is None)
	peer_list = {}

	def __init__(self):
		NICK = raw_input("What is your nick?")
		
		# Initate contact with the bootstrap, send nick, and add to lists
		BOOTSTRAP_CONNECTION = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		BOOTSTRAP_CONNECTION.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		BOOTSTRAP_CONNECTION.connect(self.ADDR)
		BOOTSTRAP_CONNECTION.sendall(b'n'+NICK)
		self.peer_list['bootstrap'] = (self.ADDR, BOOTSTRAP_CONNECTION)
		print("Connected to bootstrap")

		# Start a handler thread for bootstrap
		BOOTSTRAP_THREAD = Thread(target=self.handle_peer_client, args=('bootstrap',))
		BOOTSTRAP_THREAD.daemon = True
		BOOTSTRAP_THREAD.start()

		# Start a menu thread for client
		MENU_THREAD = Thread(target=self.client_menu)
		MENU_THREAD.daemon = True
		MENU_THREAD.start()

		# Start an accept thread for incoming peers
		ACCEPT_SOCKET = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		ACCEPT_SOCKET.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		ACCEPT_SOCKET.bind((HOST, INC_PORT))
		ACCEPT_SOCKET.listen(5)
		print("Waiting for connection...")
		ACCEPT_THREAD = Thread(target=self.accept_incoming_connections_client, args=(ACCEPT_SOCKET,))
		ACCEPT_THREAD.daemon = True
		ACCEPT_THREAD.start()

		# Wait for menu thread, then close
		MENU_THREAD.join()
		ACCEPT_SOCKET.close()
		BOOTSTRAP_CONNECTION.close()


	def handle_peer_client(self, nick):
		#Retreive the socket object via nick
		peer_socket = self.get_socket(nick)
		while True:
			try:
				# Decoding the message
				msg = peer_socket.recv(self.BUFSIZ)
				flag = msg[:1].decode()
				content = msg[1:].decode()

				if flag == 'u':	
					for peer in self.peer_list:
						print("Sending peer: %s" % peer)
						peer_socket.send(bytes(('p' + bytes((nick, self.get_ip(peer))))))
				# Accept incoming peer info
				if flag == 'p':
					print("Accepting peer %s" % content)
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

	def client_menu(self):
		while True:
			print("[W]hos online?")
			print("[U]pdate list")
			print("[C]onnect to user")
			print("[Q]uit")
			ans = raw_input()
			if ans == 'w' or ans == 'W':
				self.print_peer_list()
			if ans =='u' or ans == 'U':
				try:
					print("Update in progress...")
					b_socket = self.get_socket('bootstrap')
					b_socket.sendall(b'u')
				except:
					pass

			if ans == 'c' or ans == 'C':
				self.print_peer_list()
				peer = raw_input("Who do you want to chat with?")
				if peer in self.peer_list:
					self.connect_to_peer(peer)
				else:
					print("User not found")
			if ans == 'q' or ans == 'Q':
				return

	def connect_to_peer(self, nick):
		# Initate contact with the bootstrap, send nick, and add to lists
		PEER_CONNECTION = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		PEER_CONNECTION.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		PEER_CONNECTION.connect(self.ADDR)
		PEER_CONNECTION.sendall(b'n'+self.NICK)
		self.peer_list[nick] = (self.ADDR, PEER_CONNECTION)
		print("Connected to %s" % nick)

	#Function that starts a new thread for every new connection.
	def accept_incoming_connections_client(self, incoming_socket):
		"""Sets up handling for incoming clients."""
		while True:
			try:
				# Accepts incoming connection and adds it to peer list
				peer_socket, peer_address = bootstrap_socket.accept()
				nick = self.get_nick(peer_socket)
				print("%s:%s has connected" % peer_address)
				print("Nick: %s" % nick)
				self.peer_list[nick] = (peer_address, peer_socket)
				# Starts a handler for new peer
				Thread(target=self.handle_peer_bootstrap, args=(nick,)).start()
			except KeyboardInterrupt:
				return	

	def print_peer_list(self):
		for peer in self.peer_list:
			print(str(peer))
	def get_socket(self, nick):
		(_, socket) = self.peer_list[nick]
		return socket
	
	def get_ip(self, nick):
		(ip, _) = self.peer_list[nick]
		(adr, _) = ip
		return adr


if __name__ == "__main__":
	Client()