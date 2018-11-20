from py2p import mesh, base
import random
import time

socket = random.randint(4000, 5000)
socket2 = random.randint(4000, 5000)

sock = mesh.MeshSocket('0.0.0.0', socket)
sock = mesh.MeshSocket('0.0.0.0', 4444, out_addr=('0.0.0.0', 4456))
sock.connect('0.0.0.0', socket)
switch = 1
@sock.once('connect')
def call_once(conn):
     # conn is a reference to the socket, in case you're in a new scope
     # the .once() indicates that this event should only be called once
    print "connected"
    pass

while(True):
    sock.send('test msg')
    print "sent test msg";
    switch = 0
    msg = sock.recv()
    print(msg)
    time.sleep(1)
