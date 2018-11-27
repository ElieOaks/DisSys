##Server


"""
This is the server

"""
#!/usr/bin/env python3
import socket


class Server:

    list_of_clients = []
    list_of_connected_clients = []
    

    def give_me_IP(user_name):
        return 0

    def give_me_public_key(user_name):
        return 0

    def store_outgoing_messages(message, to_user, from_user):
        return 0

    def update_my_IP(user, new_IP):
        return 0

    def event_loop(incoming_event, from_user):
        return 0



def main():
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12342              # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port

    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print 'Got connection from', addr
        c.send('Thank you for connecting')
        c.close()                # Close the connection

if __name__ == "__main__": main()
    
