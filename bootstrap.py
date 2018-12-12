#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket as sock
from threading import Thread
import time as t
import sys
import random
import cPickle as pickle
import menu as men

class Bootstrap:
	NICK = ''
	HOST = ''
	PORT = 33000
	BUFSIZ = 4096
	ADDR = (HOST, PORT)
	PUBLIC_KEY = 1

	# Dictionary with nick as key, references IP and socket (if no connection established, socket is None)
	# peer_list[nick] = (adr, listening_port, public_key, socket_object)
	peer_list = {}

	def __init__(self):			
		ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
		ACCEPT_THREAD.daemon = True
		ACCEPT_THREAD.start()
		ACCEPT_THREAD.join()


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
				ip, _ = peer_address
				print("%s has connected" % ip)
				msg = peer_socket.recv(self.BUFSIZ)
				nick = pickle.loads(msg)
				print("Nick: " + nick)
				listening_port = peer_socket.recv(self.BUFSIZ)
				listening_port = listening_port[1:5]
				#listening_port = listening_port.rstrip('\n')
				listening_port = int(listening_port)
				print("Client's listening port: " + str(listening_port))
				self.peer_list[nick] = (ip, listening_port, self.PUBLIC_KEY, peer_socket)
				# Starts a handler for new peer
				Thread(target=self.handle_peer_client, args=(nick,)).start()
			except KeyboardInterrupt:
				print("Failed to connect to a client")
				ACCEPT_SOCKET.close()
				return


	def handle_peer_bootstrap(self, nick):
		#Retreive the socket object via nick
		peer_socket = self.get_from_peer(nick, 'socket')
		while True:
			print("Waiting for messages...")
			# Decoding the message
			payload = peer_socket.recv(self.BUFSIZ)
			(flag, content) = pickle.loads(payload)

			# Send peer peer list
			if flag == 'u':
				payload = self.create_sendable_peer_list()
				data = ('p', payload)
				peer_socket.sendall(pickle.dumps(data))
			
			# Accept incoming peer list, add peers that don't exist in peer list
			if flag == 'p':
				print("I received a peer list: " + str(content))
				for entry in content:
					if entry not in self.peer_list:
						self.peer_list[entry] = content[entry]

	def get_from_peer(self, nick, argument):
		(ip, listening_port, public_key, socket) = self.peer_list[nick]
		print "You are trying to get from peer: ",
		print str(ip) + ", " + str(listening_port) + ", " + str(public_key) + ", " + str(socket)
		switcher = {
			'ip': ip,
			'port': listening_port,
			'key': public_key,
			'socket': socket
		}
		return switcher[argument]

	def update_peer(self, nick, argument, new_value):
		(ip, listening_port, public_key, socket) = self.peer_list[nick]
		if argument == 'ip':
			self.peer_list[nick] = (new_value, listening_port, public_key, socket)
		elif argument == 'port':
			self.peer_list[nick] = (ip, new_value, public_key, socket)
		elif argument == 'key':
			self.peer_list[nick] = (ip, listening_port, new_value, socket)
		elif argument == 'socket':
			self.peer_list[nick] = (ip, listening_port, public_key, new_value)
		else:
			print("Invalid argument")

	def create_sendable_peer_list(self):
		copy = self.peer_list.copy()
		for entry in copy:
			copy[entry] = self.scrub_socket(copy[entry])
		return copy
        
	def scrub_socket(self, entry):
		(ip, port, key, socket) = entry
		return (ip, port, key, None)

	def print_peer_list(self):	
		print(str(self.peer_list))

	def get_peers(self):
		return self.peer_list.keys()


if __name__ == "__main__":
	Bootstrap()
