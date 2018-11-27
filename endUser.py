##Class for a node
import socket
import text_messages as mes

class Client:
    
    def __init__(self, identity, server_connection, my_IP):
        self.ID = identity
        self.connected = server_connection
        self.IP = my_IP
        self.text_thread = mes.text_messages([])
      
    def login(username, password):
        return 0

    #creates object text and adds it to the text_messages which is the cyrrent conversation
    def send_message(self, message, recipient):
        from_user = self.ID
        self.text_thread.add_message(message, from_user, recipient, 0)
        return 0

    #creates object text and adds it to the text_messages which is the cyrrent conversation
    def recieved_message(self, cipher_text, sender):
        message = cipher_text
        self.text_thread.add_message(message, sender, self.ID, 0)
        return 0

    def ping_server():
        return 0

    #prints out all the messages in terminal
    def show_messages(self):
        self.text_thread.show_messages()

    def ping_user():
        return 0

    #saves all the messages in a text file with the name of the user
    def save_state(self):      
        name = self.ID + ".txt"
        f= open(name,"w+")
        f.write("%s\n" % self.ID)
        f.write("%d\n" % self.connected)
        f.write("%s\n" % self.IP)
        self.text_thread.loggout(f)
        f.close()

    def loggout(self):
        self.save_state()

    #If this user has a txtx file on current device, will open that. Otherwise loggs in as a new user.
    def loggin(self, file_name):
        try:
            f = open(file_name, "r")
        except:
            self.new_user()
            return
        
        self.ID = f.readline().rstrip('\n')
        self.connected = int(f.readline().rstrip('\n'))
        self.IP = f.readline().rstrip('\n')        
        self.text_thread.loggin(f)
        f.close()

    #createsa new user, has some flaws. 
    def new_user(self):
        identity = raw_input("Choose a username: ")
        
        self.ID = identity
        self.connected = False
        self.IP = "000.000.000.000"
        self.text_thread = mes.text_messages([])
        self.save_state()
        
        
        
        
    def eventloop(incoming_event):
        return 0

#small program to test stuff out
"""def main():
    person = raw_input('Enter your username: ')

    do = Client(None, None, None)
    do.loggin(person+".txt")

    inp = raw_input(person + ": ")
    while(inp != 'q'):
        if (inp == 'p'):
            do.show_messages()
        do.send_message(inp, "Karin")
        inp = raw_input(person + ": ")

    do.loggout()
    
    print("Thank you " + person + " for using Sexy People Talk, where all sexy people can talk!")"""

def main():

    s = socket.socket()        # Create a socket object
    host = socket.gethostname() # Get local machine name
    print host
    port = 12342               # Reserve a port for your service.

    s.connect((host, port))
    print s.recv(1024)
    s.close                     # Close the socket when done
    


if __name__ == "__main__": main()
        
    

