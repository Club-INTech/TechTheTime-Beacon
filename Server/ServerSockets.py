import socket
import time
from threading import Thread
import queue


def create_socket(ip, port):
    new_socket = socket.socket()
    new_socket.bind((ip, port))
    new_socket.listen(5)
    new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return new_socket


class SocketServer(Thread):
    def __init__(self, ip, port, side):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.side = side
        self.socket = create_socket(ip, port)
        self.socket.settimeout(0.5)
        self.con = None

    def handle(self):
        pass

    def set_connected(self, con):
        pass

    def run(self):
        print("Port {} is ready for connection...".format(self.port))
        while self.side.channel.isRunning:
            # print(self.side.channel.isRunning)
            if not self.side.is_connected():
                try:
                    (self.con, (ip, port)) = self.socket.accept()
                    self.con.settimeout(0.5)
                    self.set_connected(True)
                    print("Client {}:{} connected".format(ip, port))
                except socket.timeout:
                    pass
            else:
                try:
                    # print("Handle...")
                    self.handle()
                    # print("Handle done...")
                except socket.timeout as e:
                    pass
                time.sleep(0.5)

        self.side.disconnect()
        # self.set_connected(False)
        # self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print('Socket closed, bye !')


# Receiving data from client
class InputSocket(SocketServer):
    def __init__(self, ip: str, port: int, side, callback):
        SocketServer.__init__(self, ip, port, side)
        self.callback = callback

    def handle(self):
        # print("Waiting for message on port {}...".format(self.port))
        msg = self.con.recv(1024)
        if msg == b'0':
            # self.set_connected(False)
            self.side.disconnect()
            print('Client on port {} disconnected'.format(self.port))
        elif msg == b'':
            print('a')
        else:
            self.callback(msg)
            print('Data received : {}'.format(msg))

    def set_connected(self, con):
        # print('Connected: {}'.format(con))
        self.side.isInputConnected = con
        # print('Client connected: {}'.format(self.side.is_connected()))


# Sending data to client
class OutputSocket(SocketServer):
    def __init__(self, ip, port, side):
        SocketServer.__init__(self, ip, port, side)
        self.sending_buffer = queue.Queue()

    def send(self, data):
        if self.side.is_connected():
            try:
                self.con.send(data)
                print('Data sent: {}'.format(data))
            except socket.timeout as e:
                self.sending_buffer.put(data)
                print('Timeout : {}'.format(e))
        else:
            self.sending_buffer.put(data)
            print('No client connected to send {}'.format(data))

    def set_connected(self, con):
        # print('Connected {}'.format(con))
        self.side.isOutputConnected = con
        # print('Client connected: {}'.format(self.side.is_connected()))

    def handle(self):
        if not self.sending_buffer.empty():
            self.send(self.sending_buffer.get())

