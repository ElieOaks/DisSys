import socket
import threading
import sys
import time
from random import randint

class Server:
    #AF_INET = IPv4, SOCK_STREAM = TCP
    connections = []
    peers = []

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to an IP address and port
        sock.bind(('0.0.0.0', 10000))
        #Defina max nr of connections
        sock.listen(1)
        print("Server running...")

        while True:
            # C = connection, A = connection address
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))

            # Allows program to exit even when there's active threads
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0]) + ':' + str(a[1]), "connected")
            self.sendPeers()

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(bytes(data))
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c) 
                self.peers.remove(a[0])
                c.close
                self.sendPeers()
                break

    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ","
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, 'utf-8'))

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, 10000))

        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))

        
    def sendMsg(self, sock):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def updatePeers(self, peerData):
        p2p.peers = str(peerData, 'utf-8').split(",")[:-1]


class p2p:
    peers = ['127.0.0.1']

while True:
    try:
        print("Trying to connect ...")
        time.sleep(randint(1, 5))
        for peer in p2p.peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            try:
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("Couldn't start server ...")
    except KeyboardInterrupt:
        sys.exit(0)




