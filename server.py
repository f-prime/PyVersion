#!/usr/bin/python
import socket, os, sys, threading

class server:
    def __init__(self):
        self.port = int(sys.argv[1])
        self.cmds = {

                "send":self.send,
                "get":self.get,
                "del":self.dele,
                "list":self.list,

                }
    def main_loop(self):
        sock = socket.socket()
        sock.bind(('', self.port))
        sock.listen(5)
        while True:
            self.obj, conn = sock.accept()
            print conn[0]
            data = self.obj.recv(1024)
            self.data = data
            try:
                self.file = data.split()[1]
            except:
                pass

            try:
                threading.Thread(target=self.cmds[data.split()[0]]).start()
            except:
                pass
    def send(self):
        with open(self.file, 'wb') as file:
            while True:
                data = self.obj.recv(1024)
                if not data:
                    self.obj.close()
                    break
                file.write(data)

    def list(self):
        curdir = os.listdir(os.getcwd())
        curdir.remove(sys.argv[0])
        self.obj.send(str(curdir))
        self.obj.close()

    def get(self):
        try:
            file = self.data.split()[1]
            with open(file, 'rb') as file:
                for line in file.readlines():
                    self.obj.send(line)
            self.obj.close()
        except IOError:
            self.obj.send("File does not exist")
            self.obj.close()

    def dele(self):
        try:
            file = self.data.split()[1]
            os.remove(file)
            self.obj.close()
        except OSError:
            self.obj.send("File does not exist.")
            self.obj.close()

if __name__ == "__main__":
    try:
        server().main_loop()
    except IndexError:
        print "Usage: python server.py <port>"

