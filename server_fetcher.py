from models import *

import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 12345
BUFFER_SIZE = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
while True:
    conn, addr = s.accept()
    print("Connection from {}".format(addr))
    data = conn.recv(BUFFER_SIZE)
    if "FETCH" not in data:
        continue
    time = data[6:]
    print("Fetching messages since {}".format(data))
    messages = session.query(Message).filter(Message.timestamp > int(time)).all()
    print("\n".join([m.message for m in messages]))
    conn.send("\n".join([m.message for m in messages]))
    conn.send("END_MESSAGE")
    print("Response sent")