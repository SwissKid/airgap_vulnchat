#!/usr/bin/python2
import socket
import pickle
import base64
import arrow

class Server:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def _udp_packet(self, packet):
        self.udp_socket.sendto(packet, (self.hostname, self.port))

    def fetch(self, lasttime):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect((self.hostname, self.port))
        self.tcp_socket.send("FETCH {}".format(lasttime))
        data_back = ""
        while True:
            data_back += self.tcp_socket.recv(20)
            if "END_MESSAGE" in data_back:
                break
        # print("GOT {} BACK".format(data_back))
        self.tcp_socket.close()
        return data_back
    def send_message(self, msg):
        self._udp_packet(pickle.dumps(msg))
        msg.sent = True


class Message:
    def __init__(self, message, to, msg_from):
        self.message = message
        self.to = to
        self.msg_from = msg_from
        self.sent = False

class Client:
    def __init__(self, name, hostname, port, start=arrow.now):
        self.server = Server(hostname, port)
        self.name = name
        self.last_check = start
        self.run()
    
    def check_messages(self):
        data = self.server.fetch(self.last_check.timestamp)
        data = data.replace("END_MESSAGE","")
        for item in data.split("\n"):
            if item == "":
                continue
            # print("|{}|".format(item))
            try:
                mes = pickle.loads(base64.b64decode(item))
            except:
                print("Corrupted Message")
                continue
            if mes.to == self.name:
                print("{} : {}".format(mes.msg_from, mes.message))

        self.last_check = arrow.now()
    
    def run(self):
        while True:
            print("1=Check message, 2=send message")
            answer = raw_input()
            if answer == "1":
                self.check_messages()
            if answer == "2":
                self.send_message()
    
    def send_message(self):
        to = raw_input("To:")
        msg = raw_input("Message:")
        new_msg = Message(msg, to, self.name)
        self.server.send_message(new_msg)



if __name__ == "__main__":
    name = raw_input("Your Handle:")
    Client(name, "localhost", 12345, arrow.get(0))