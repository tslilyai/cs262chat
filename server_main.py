'''
The main function to start and run the server lives here!
'''
import sys
from protobuf.protobuf_server import run as run_protobuf
#import custom.custom_server 

def main():
    protocol = sys.argv[1]
    print "protocol is", protocol
    port = sys.argv[2]

    if protocol == "protobuf":
        run_protobuf(port)
        print "Running protobuf server"
    if protocol == "custom":
        custom_server.run(port)

if __name__ == '__main__':
    main()
