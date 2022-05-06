import socket
import sys
import time
from threading import Thread
from signal import *

from ServerChannel import ServerChannel
from ServerSockets import *


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <ip address> <connections>")
        sys.exit(1)

    channels = [ServerChannel(sys.argv[1], int(con[0]), int(con[1]), int(con[2])) for con in sys.argv[2:]]

    for channel in channels:
        channel.start()

        for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
            signal(sig, lambda signum, frame: channel.stop())

