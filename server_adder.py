from models import *

import socket
import arrow
import base64

UDP_IP = "127.0.0.1"
UDP_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(99999999) # buffer size is 1024 bytes
    print("Received {}".format(data))
    message = Message(message=base64.b64encode(data), timestamp=arrow.now().timestamp)
    session.add(message)
    session.commit()