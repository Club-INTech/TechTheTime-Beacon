from ServerSide import *


class ServerChannel:
    def __init__(self, ip: str, a_id: int, b_id: int, con_id: int):
        self.a_id = a_id
        self.b_id = b_id
        self.a_side = ServerSide(ip, 5000 + 100 * a_id + 10 * b_id + con_id,
                                 6000 + 100 * a_id + 10 * b_id + con_id, self, 'A', lambda msg: self.send_to_b(msg))
        self.b_side = ServerSide(ip, 5000 + 100 * b_id + 10 * a_id + con_id,
                                 6000 + 100 * b_id + 10 * a_id + con_id, self, 'B', lambda msg: self.send_to_a(msg))
        self.isAConnected = False
        self.isBConnected = False
        self.isRunning = True

        print("Created connection {} between {} and {}".format(con_id, a_id, b_id))
        print("Available ports: {} and {}".format(self.a_side.i_port, self.b_side.i_port))

    def start(self):
        self.a_side.start()
        self.b_side.start()

    def close(self):
        self.isRunning = False
        self.a_side.stop()
        self.b_side.stop()

    def join(self):
        self.a_side.inputSocket.join()
        self.a_side.outputSocket.join()
        self.b_side.inputSocket.join()
        self.b_side.outputSocket.join()

    def stop(self):
        self.a_side.send(b'0')
        self.b_side.send(b'0')
        self.isRunning = False

    # def shutdown(self, how):
    #     self.a_input_socket.socket.shutdown(how)
    #     self.a_output_socket.socket.shutdown(how)
    #     self.b_input_socket.socket.shutdown(how)
    #     self.b_output_socket.socket.shutdown(how)

    def send_to_a(self, msg):
        print("Sending to {}: {}".format(self.a_id, msg))
        self.a_side.send(msg)

    def send_to_b(self, msg):
        print("Sending to {}: {}".format(self.b_id, msg))
        self.b_side.send(msg)
