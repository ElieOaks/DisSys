import text_messages as mes
import text as tx

class Message_Interface:

    # Param nick: Nickname of the messanger
    # Param private_key: The RSA key that this user encrypts messages with.
    # Param public_key: The key used by others to decrypt this messangers messages.
    # Initiates the list of messages with one peer
    def __init__(self, nick, private_key, public_key, friend_pub_key, friend_nick):
        self.nick = nick
        self.__pri_key = private_key
        self.__pub_key = public_key
        self.__friend_pub_key = friend_pub_key
        self.__friend_nick = friend_nick
        self.__text_thread = mes.text_messages([])


    # Adds a message to the message list
    # returns a message package that contains (ciphertext, reciever_nick)
    def encrypt_message_to_send(self, text, to_nick):
         message = self.__text_thread.add_text(text, self.nick, to_nick)
         #TODO encrypt message with private key and recievers public key
         #TODO use get_message to set the messages cipher text in the message
         return (message.get_text, to_nick, self.nick)

    # decrypts incoming messages, and adds it to the message list
    def decrypt_message_recieved(self, text, from_nick):
         cipher_text = text
         #TODO: decrypt message with private key and friends public key and handling if it failed
         decrypted_text = cipher_text
         self.__text_thread.add_text(decrypted_text, from_nick, self.nick)

    def get_friend(self):
        return self.__friend_nick

    # prints all the messages in this thread
    def show_all_messages(self):
        self.__text_thread.show_messages()

    # prints the last 10 messages in this thread
    def show_last_ten_messages(self):
        self.__text_thread.show_last_messages()


    #saves all the messages to a local file called nick.txt
    def save_state_local(self, friend_nick):
        name = ".\conversations\\" + friend_nick + self.nick + ".txt"
        print name
        f= open(name,"w+")
        f.write("%s\n" % self.nick)
        f.write("%d\n" % self.__pri_key)
        f.write("%s\n" % self.__pub_key)      
        f.write("%s\n" % self.__friend_pub_key)
        f.write("%s\n" % self.__friend_nick)
        self.__text_thread.save_state(f)
        f.close()

    # Loads messages from local file called nick.txt
    def recover_local_state(self, file):
        try:
            f = open(file, "r")      

            self.nick = f.readline().rstrip('\n')
            self.__pri_key = int(f.readline().rstrip('\n'))
            self.__pub_key = f.readline().rstrip('\n')
            self.__friend_pub_key = f.readline().rstrip('\n')
            self.__friend_nick = f.readline().rstrip('\n')

            self.__text_thread.recover_state(f)

            f.close()
            print("state recovered")
            return self.__friend_nick
        except:
            print("recovering state failed!")
            return -1
