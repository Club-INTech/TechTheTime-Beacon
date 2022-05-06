# Used to read parameters from the launch file.
import sys
# Used to make pauses.
from time import sleep
# Used to read signals.
from signal import *

# What you need to import to create clients !
from ClientChannel import *

# Create two clients : the first one will be used to connect to channel 010 from 0, so we pass first the ip address,
# then the origin, which is itself, 0,
# then the destination, which is the other client, 1, and finally the id of the connection. Usually 0 or 1.
# Lastly we pass a lambda function that will be called when a message is received.
# This function takes a bytes as parameter.
# Example : ClientChannel("192.168.0.10", 0, 1, 0, lambda x: print(x))
cli0 = ClientChannel(sys.argv[1], 0, 1, int(sys.argv[2]), lambda msg: print("0 received from 1 : " + str(msg)))
cli1 = ClientChannel(sys.argv[1], 1, 0, int(sys.argv[2]), lambda msg: print("1 received from 0 : " + str(msg)))

# This function is just called if we want to stop the program.
def stop_all():
    print("\nStopping...")
    cli0.stop()
    cli1.stop()
    return

# We register the function to be called when we want to stop the program.
for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, lambda nb, stack: stop_all())

# We start the clients.
cli0.start()
cli1.start()

# We send message from one client to the other one.
cli0.send(b"0: Hello")
cli1.send(b"1: How are you bro ?")

# We wait for the clients to stop.
# sleep(2)
#
# cli0.stop()
# cli1.stop()

