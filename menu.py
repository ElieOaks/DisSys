import Message_interface as mes
import os
import threading

class User:

    def __init__(self, nick, client):
        self.nick = nick
        self.conversations = []
        self.client = client

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
        new_message_thread = mes.Message_Interface(self.nick, 0, 0, 0, friend_nick)        
        self.conversations.append((friend_nick, new_message_thread))
        return new_message_thread

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
                conv.decrypt_message_to_send
                print("Does it work?")
                self.client.send_message(text, to_nick)
                
    def quit(self):
        for (user, conv) in self.conversations:
            print user
            conv.save_state_local(user)

class Menu:

    def __init__(self, user):
        self.user = user
        self.nick = user.nick

    def dis_menu(self):
        print(" [O]pen conversations")
        print(" [Q]uit")

        inp = raw_input(">> ")
        if (inp == 'Q' or inp == 'q'):
            self.user.quit()
            return None
        elif (inp == 'O' or inp == 'o'):
            self.user.print_conversation_holders()
            friend_nick = raw_input("Who do you want to talk to?")
            return self.user.get_conversation(friend_nick)

def loggin(nick, client):
    us = User(nick, client)
    for files in os.listdir("./conversations"):
        for file in files:
            if file.endswith(us.nick + ".txt"):
                new_message_thread = mes.Message_Interface(nick, 0, 0, 0, "temp")
                friend_nick = new_message_thread.recover_local_state(file)
                if (result != -1):
                    user.add_conversation(friend_nick, new_message_thread)
    return us

def talk(user):
    menu = Menu(user)
    choice = menu.dis_menu()

    while(choice != None):
        inp = raw_input(">>  ")
        if (inp == "menu"):
            choice = menu.dis_menu()
        else:            
            message = choice.encrypt_message_to_send(inp, choice.get_friend())
            user.client.send_message(inp, user.nick, choice.get_friend)
            #TODO: send message to other client

def listen(user):
    i = 100000000
    while(i > 0):
        if (i == 5 or i == 10000):
            user.add_recieved_text("Can you not read my messages?", "Hanna")
        i = i-1
        


def main(client):
    nick = raw_input("What is your username?")
    user = loggin(nick, client)

    thread2 = threading.Thread(target=listen, args=[user])
    #listen(user)
    thread2.start()

    talk(user)
    user.quit()
    
