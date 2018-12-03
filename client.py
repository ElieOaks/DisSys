#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket as sock
from threading import Thread
import time
import sys

class Client:
	NICK = ''
	HOST = ''
	PORT = 33000
	BUFSIZ = 1024
	ADDR = (HOST, PORT)

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

		# Wait for menu thread, then close
		MENU_THREAD.join()
		BOOTSTRAP_CONNECTION.close()


	def handle_peer_client(self, nick):
		#Retreive the socket object via nick
		peer_socket = self.get_socket(nick)
		while True:
			try:
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
					self.peer_list[nick] = content
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
			print("[Q]uit")
			ans = raw_input()
			if ans == 'w' or ans == 'W':
				print(str(self.peer_list))
			if ans =='u' or ans == 'U':
				try:
					print("Update in progress...")
					b_socket = self.get_socket('bootstrap')
					b_socket.sendall('u')
				except:
					pass
			if ans == 'q' or ans == 'Q':
				return

	def get_socket(self, nick):
		(_, socket) = self.peer_list[nick]
		return socket


if __name__ == "__main__":
	Client()