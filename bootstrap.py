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
		# Start the thread which listens for connections
		ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
		ACCEPT_THREAD.daemon = True
		ACCEPT_THREAD.start()
		ACCEPT_THREAD.join()

#Function that starts a new thread for every new connection.
	def accept_incoming_connections(self):
		"""Sets up handling for incoming clients."""
		ACCEPT_SOCKET = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		ACCEPT_SOCKET.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		ACCEPT_SOCKET.bind(self.ADDR)
		ACCEPT_SOCKET.listen(5)
		print("Waiting for connection...")
		while True:
			try:
				# Accepts incoming connection and adds it to peer list
				peer_socket, peer_address = ACCEPT_SOCKET.accept()
				nick = self.get_nick(peer_socket)
				print("%s:%s has connected" % peer_address)
				print("Nick: %s" % nick)
				self.peer_list[nick] = (peer_address, peer_socket)
				# Starts a handler for new peer
				Thread(target=self.handle_peer_client, args=(nick,)).start()
			except KeyboardInterrupt:
				ACCEPT_SOCKET.close()
				return

	# Gets the nick
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


	def connect_to_peer(self, nick):
		# Initate contact with the bootstrap, send nick, and add to lists
		PEER_CONNECTION = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		PEER_CONNECTION.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
		PEER_CONNECTION.connect((self.get_ip(nick), self.PORT))
		PEER_CONNECTION.sendall(b'n'+self.NICK)
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
						(inc_nick, ip) = eval(content)
						print("Accepting peer: %s at ip: %s" %inc_nick, ip)
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

	def print_peer_list(self):
		for peer in self.peer_list:
			print(str(peer))
	
	def get_socket(self, nick):
		(_, socket) = self.peer_list[nick]
		return socket
	
	def get_ip(self, nick):
		(ip, _) = self.peer_list[nick]
		return ip
	
	def split_peers(self, messages):
		payload = messages.split('p(')
		print(str(payload))
		for peer in payload:
			peer = '(' + peer
		return payload




if __name__ == "__main__":
	Bootstrap()
