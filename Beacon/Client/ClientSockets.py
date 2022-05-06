import socket
import time
from threading import Thread
import queue


class ClientSocket(Thread):
    def __init__(self, host: str, port: int, channel):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.channel = channel
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(0.5)

    def set_connected(self, connected: bool):
        pass

    def get_connected(self):
        pass

    def connect(self):
        if not self.get_connected():
            try:
                self.socket.connect((self.host, self.port))
                self.set_connected(True)
                print('Connected to ' + self.host + ':' + str(self.port))
            except socket.error as e:
                # print("Socket error : " + str(e))
                pass

    def handle(self):
        pass

    def run(self):
        while self.channel.isRunning:
            if not self.get_connected():
                self.connect()
                time.sleep(1)
            elif self.channel.is_connected():
                try:
                    self.handle()
                except socket.timeout:
                    continue
                except socket.error as e:
                    print("Socket error : " + str(e))
                    self.channel.stop()

        self.set_connected(False)
        # self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print('Socket closed, bye !')


class InputSocket(ClientSocket):
    def __init__(self, host: str, port: int, channel, callback: callable(bytes)):
        ClientSocket.__init__(self, host, port, channel)
        self.callback = callback

    def set_connected(self, connected: bool):
        self.channel.isInputConnected = connected

    def get_connected(self):
        return self.channel.isInputConnected

    def handle(self):
        msg = self.socket.recv(1024)
        print('Received : ' + str(msg))
        if msg == b'0' or msg == b'':
            print('Server disconnected')
            self.set_connected(False)
            # time.sleep(5)
        else:
            print('Data received : {}'.format(msg))
            self.callback(msg)


class OutputSocket(ClientSocket):
    def __init__(self, host: str, port: int, channel):
        ClientSocket.__init__(self, host, port, channel)
        self.sending_buffer = queue.Queue()

    def set_connected(self, connected: bool):
        self.channel.isOutputConnected = connected

    def get_connected(self):
        return self.channel.isOutputConnected

    def send(self, msg):
        if self.channel.is_connected():
            self.socket.send(msg)
            print('Data sent to port {}: {}'.format(self.port, msg))

    def handle(self):
        if not self.sending_buffer.empty():
            self.send(self.sending_buffer.get())
