import Message_interface as mes
import os
import threading
import pickle
import client
import time as t

class User:

	def __init__(self, nick, client):
		self.nick = nick
		self.conversations = []
		self.client = client
        self.message = []

	def add_conversation(self, friend_nick, message_thread):  
		self.conversations.append((friend_nick, message_thread))

	def print_conversation_holders(self):
		for (user, conv) in self.conversations:
			print user

	def get_conversation(self, friend_nick):
		for (user, conv) in self.conversations:
			if user == friend_nick:
				conv.show_all_messages()
				return conv 
		return False
        def get_friend(self, friend_nick):
		for (user, conv) in self.conversations:
			if user == friend_nick:
				conv.show_all_messages()
				return user
		return False


	def add_recieved_text(self, text, from_nick):
		 for (user, conv) in self.conversations:
			if user == from_nick:
				conv.decrypt_message_recieved(text, from_nick)
				return
		 new_message_thread = mes.Message_Interface(self.nick, 0, 0, 0, from_nick)        
		 self.conversations.append((from_nick, new_message_thread))
		 new_message_thread.decrypt_message_recieved(text, from_nick)

	def add_text(self, text, to_nick):
	        for (user, conv) in self.conversations:
			if user == to_nick:
				conv.encrypt_message_to_send(text, to_nick)
				return self.client.send_message(text, self.nick, to_nick)

	def update_conversation_list(self):
		friends = self.client.get_peers()
		for friend in friends:
			x = False
                        if friend != "bootstrap" or friend != self.nick:
			   for user, conv in self.conversations:
				if friend == user:
					x = True
	                   if not x:
				new_message_thread = mes.Message_Interface(self.nick, 0, 0, 0, friend)        
				self.conversations.append((friend, new_message_thread))
					       
	def quit(self):
		for (user, conv) in self.conversations:
			print user
			conv.save_state_local(user)

class Menu:

	def __init__(self, user):
		self.user = user
		self.nick = user.nick

	def dis_menu(self):
		while True:
			print(" [O]pen conversations")
			print(" [W]hos online")
			print(" [Q]uit")

			inp = raw_input(">> ")
			if (inp == 'Q' or inp == 'q'):
				self.user.quit()
				return None
			elif (inp == 'O' or inp == 'o'):
				self.user.update_conversation_list()
				t.sleep(3)
				self.user.print_conversation_holders()
				friend_nick = raw_input("Who do you want to talk to?")
				result = self.user.get_conversation(friend_nick)
				if not result:
					print ("That friend is not online")
                                elif (friend_nick == self.nick or friend_nick == "bootstrap"):
                                        print "This is for conversations, not notes."
				else:
					return friend_nick

			elif inp =='u' or inp == 'U':
				print("Update in progress...")
				self.user.client.update_peer_list()
			elif inp == 'w' or inp == 'W':
				self.user.update_conversation_list()
				self.user.print_conversation_holders()


def loggin(user):
	us = user
	for file in os.listdir("./conversations"):
		if file.endswith(us.nick + ".txt"):
			friend_nick = str(file).rstrip(us.nick + ".txt")
			print ("File name has friend: " + friend_nick)
			new_message_thread = mes.Message_Interface(us.nick, 0, 0, 0, friend_nick)
			success = new_message_thread.recover_local_state(friend_nick)
			if (success != -1):
				user.add_conversation(friend_nick, new_message_thread)
	return us

def talk(user):
	menu = Menu(user)
	loggin(user)
	choice = menu.dis_menu()

	while(choice != None):
		inp = raw_input(">>  ")
		if (inp == "menu"):
			choice = menu.dis_menu()
		else:              
			user.add_text(inp, choice)
		


def main(user):
	talk(user)
	user.quit()
	
