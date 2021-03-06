'''
The main function to start and run the server lives here.

This runs the server-side application, which listens to calls from the client application
via the specified protocol, and communicates with the database in order to store and retrieve
client information.

Logs of all server calls and responses are printed to console.

Usage: python server_main.py --protocol [default:protobuf] --port [default:8080]
'''
import argparse

from protobuf.protobuf_server import run as run_protobuf
from custom.custom_server import run as run_custom

def main():
    parser = argparse.ArgumentParser(description='Chat client.')
    parser.add_argument('--protocol', dest='protocol', action='store',
            default='protobuf', help='Protocol to use (default=protobuf)')
    parser.add_argument('--port', dest='port', action='store',
            default='8080', help="Server's port (default=8080)")
    args = parser.parse_args()

    print "protocol is", args.protocol

    if args.protocol == "protobuf":
        run_protobuf(int(args.port))
        print "Running protobuf server"
    elif args.protocol == "custom":
        run_custom(int(args.port))
        print "Running custom server"

if __name__ == '__main__':
    main()
