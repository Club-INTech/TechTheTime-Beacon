from ServerSockets import *


class ServerSide:
    def __init__(self, ip, i_port, o_port, channel, side_id, callback):
        self.ip = ip
        self.i_port = i_port
        self.o_port = o_port
        self.channel = channel
        self.side_id = side_id
        self.callback = callback

        self.inputSocket = InputSocket(self.ip, self.i_port, self, self.callback)
        self.outputSocket = OutputSocket(self.ip, self.o_port, self)

        self.isInputConnected = False
        self.isOutputConnected = False

    def is_connected(self):
        # print('Input connected: {} / Output connected: {} / Side connected: {}'.format(self.isInputConnected, self.isOutputConnected, self.isInputConnected and self.isOutputConnected))
        return self.isInputConnected and self.isOutputConnected

    def start(self):
        self.inputSocket.start()
        self.outputSocket.start()

    def send(self, msg):
        self.outputSocket.send(msg)

    def disconnect(self):
        self.outputSocket.send(b'0')
        self.isInputConnected = False
        self.isOutputConnected = False
        # self.outputSocket.socket.close()
        # self.inputSocket.socket.close()

    def stop(self):
        self.disconnect()
        self.inputSocket.join()
        self.outputSocket.join()
