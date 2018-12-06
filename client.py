#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket as sock
from threading import Thread
import time as t
import sys
import json
import random
import pickle

class Client:
	NICK = ''
	HOST = ''
	PORT = 33000
	BUFSIZ = 4096
	#ADDR = (HOST, PORT)
	IS_BOOTSTRAP = False

	# Dictionary with nick as key, references IP and socket (if no connection established, socket is None)
	peer_list = {}

	def __init__(self, IS_BOOTSTRAP):
		self.IS_BOOTSTRAP = IS_BOOTSTRAP
		# Start an accept thread for incoming peers
		if self.IS_BOOTSTRAP:
			ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
			ACCEPT_THREAD.daemon = True
			ACCEPT_THREAD.start()
			self.NICK = 'bootstrap'
			ACCEPT_THREAD.join()

		else:
			self.peer_list['bootstrap'] = ('', None)
			self.NICK = raw_input("What is your nick?")
			# Initate contact with the bootstrap, send nick, and add to lists
			self.connect_to_peer('bootstrap')

			# Start a menu thread for client
			MENU_THREAD = Thread(target=self.client_menu)
			MENU_THREAD.daemon = True
			MENU_THREAD.start()
			MENU_THREAD.join()
			


	#Function that starts a new thread for every new connection.
	def accept_incoming_connections(self):
		"""Sets up handling for incoming clients."""
		ACCEPT_SOCKET = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		ACCEPT_SOCKET.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		ACCEPT_SOCKET.bind((self.HOST, self.PORT))
		ACCEPT_SOCKET.listen(5)
		print("Waiting for connection...")
		while True:
			try:
				# Accepts incoming connection and adds it to peer list
				peer_socket, peer_address = ACCEPT_SOCKET.accept()
				print("%s:%s has connected" % peer_address)
				msg = peer_socket.recv(self.BUFSIZ)
				nick = pickle.loads(msg)
				print("Nick: " + nick)
				self.peer_list[nick] = (peer_address, peer_socket)
				# Starts a handler for new peer
				Thread(target=self.handle_peer_client, args=(nick,)).start()
			except KeyboardInterrupt:
				print("Failed to connect to a client")
				ACCEPT_SOCKET.close()
				return

	def connect_to_peer(self, nick):
		# Initate contact with the bootstrap, send nick, and add to lists
		PEER_CONNECTION = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		PEER_CONNECTION.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		PEER_CONNECTION.connect((self.get_ip(nick), self.PORT))
		t.sleep(.5)
		print("Sending nick: " + self.NICK)
		PEER_CONNECTION.sendall(pickle.dumps(self.NICK))
		self.peer_list[nick] = (self.get_ip(nick), PEER_CONNECTION)
		print("Connected to %s" % nick)

		# Start a handler thread for peer
		HANDLER_THREAD = Thread(target=self.handle_peer_client, args=(nick,))
		HANDLER_THREAD.daemon = True
		HANDLER_THREAD.start()


	def handle_peer_client(self, nick):
		#Retreive the socket object via nick
		peer_socket = self.get_socket(nick)
		while True:
			print("Waiting for messages...")
			# Decoding the message
			payload = peer_socket.recv(self.BUFSIZ)
			(flag, content) = pickle.loads(payload)

			# Send peer peer list
			if flag == 'u':
				data = ('p', self.create_peer_list())
				peer_socket.sendall(pickle.dumps(data))
			
			# Accept incoming peer list, add peers that don't exist in peer list
			if flag == 'p':
				for entry in content:
					if entry not in self.peer_list:
						(peer, address) = entry
						self.peer_list[peer] = (address, None)
			

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
				print("Update in progress...")
				b_socket = self.get_socket('bootstrap')
				msg = pickle.dumps(('u', ''))
				b_socket.sendall(msg)

			if ans == 'c' or ans == 'C':
				self.print_peer_list()
				peer = raw_input("Who do you want to chat with?")
				if peer in self.peer_list:
					self.connect_to_peer(peer)
				else:
					print("User not found")
			if ans == 'q' or ans == 'Q':
				return

	def print_peer_list(self):
		print(str(self.peer_list.keys()))
	
	def get_socket(self, nick):
		if nick not in self.peer_list:
			return None
		(_, socket) = self.peer_list[nick]
		return socket
	
	def get_ip(self, nick):
		(ip, _) = self.peer_list[nick]
		return ip

	def merge_peer_list(self, other_peer_list):
		z = self.peer_list.copy()  
		z.update(other_peer_list)
		self.peer_list = z
		
	def create_peer_list(self):
		new_list = []
		for peer in self.peer_list:
			new_list.append((peer, self.get_ip(peer)))
		return new_list


if __name__ == "__main__":
	ans = raw_input("Are you bootstrap?")
	if ans == 'y' or ans == 'Y':
		Client(True)
	else:
		Client(False)