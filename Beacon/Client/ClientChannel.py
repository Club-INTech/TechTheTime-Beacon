from ClientSockets import InputSocket, OutputSocket


class ClientChannel:
    def __init__(self, host: str, origin_id: int, destination_id: int, con_id: int, callback: callable):
        self.server_ip = host
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.con_id = con_id
        self.isInputConnected = False
        self.isOutputConnected = False
        self.isRunning = False
        self.input_socket = \
            InputSocket(host, 6000 + origin_id * 100 + destination_id * 10 + con_id, self, callback)
        self.output_socket = \
            OutputSocket(host, 5000 + origin_id * 100 + destination_id * 10 + con_id, self)

        print("Created connection {} form client {} to client {} via server {}"
              .format(con_id, origin_id, destination_id, host))

    def start(self):
        self.isRunning = True
        self.input_socket.start()
        self.output_socket.start()
        # self.connect()

    def is_connected(self):
        return self.isInputConnected and self.isOutputConnected

    def connect(self):
        self.input_socket.connect()
        self.output_socket.connect()

    def stop(self):
        self.output_socket.send(b'0')
        self.isRunning = False
        self.input_socket.join()
        self.output_socket.join()

    def send(self, msg):
        self.output_socket.send(msg)
