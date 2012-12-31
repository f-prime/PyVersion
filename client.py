#!/usr/bin/python
import socket, sys

class client:
    def __init__(self):
        self.cmd = sys.argv[1]
        self.file = sys.argv[2]
        self.ip = sys.argv[3]
        self.port = int(sys.argv[4]) 
        self.cmds = {

                "send":self.send,
                "get":self.get,
                "del":self.dele,
                "list":self.list,

                }
    def main_loop(self):
        self.sock = socket.socket()
        self.sock.connect((self.ip, self.port))
        self.cmds[self.cmd]()

    def list(self):
        self.sock.send("list")
        print self.sock.recv(1024)
        self.sock.close()

    def send(self):
        try:
            self.sock.send("send "+self.file+"\n\r\n\r")
            with open(self.file, 'rb') as file:
                for line in file.readlines():
                    self.sock.send(line)
            self.sock.close()
        except IOError:
            print "File does not exist."
            self.sock.close()



    def get(self):
        self.sock.send("get "+self.file)
        with open(self.file, 'wb') as file:
            while True:
                data = self.sock.recv(1024)
                if not data:
                    self.sock.close()
                    break
                file.write(data)

    def dele(self):
        self.sock.send("del "+self.file)
        self.sock.close()

if __name__ == "__main__":
    try:
        client().main_loop()
    except IndexError:
        print "Usage: python client.py <list|send|get|del> <file name or none is using list command> <ip> <port>"
