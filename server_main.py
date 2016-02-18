'''
The main function to start and run the server lives here!
'''
import sys
import protobuf.protobuf_server 
import custom.custom_server 

def main():
    protocol = sys.argv[1]
    port = sys.argv[2]

    if protocol == "protobuf":
        protobuf_server.run(port)
    if protocol == "custom":
        custom_esrver.run(port)
