'''
client_main.py

This runs the client application, which calls the protocol API
specified by the Protocol class in order to communicate with the server
and other clients.

Usage: python client_main.py --protocol [default:protobuf] --port [default:8080] --host [default:0.0.0.0]
'''

import argparse
import curses
import os

from frontend.application import Application
from protobuf.protobuf_client import ProtobufProtocol
from custom.custom_client import CustomProtocol

def main(screen):
    if args.protocol == 'protobuf':
        p = ProtobufProtocol(args.host, int(args.port))
    if args.protocol == 'custom':
        p = CustomProtocol(args.host, int(args.port))

    window = Application(screen, p)
    window.run()    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat client.')
    parser.add_argument('--protocol', dest='protocol', action='store',
            default='protobuf', help='Protocol to use (default=protobuf)')
    parser.add_argument('--port', dest='port', action='store',
            default='8080', help="Server's port (default=8080)")
    parser.add_argument('--host', dest='host', action='store',
            default='0.0.0.0', help="Server host (default=0.0.0.0)")

    args = parser.parse_args()

    # By default, curses delays 1 second before returning ESC to us
    # This environment variable controls the delay lag in milliseconds
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main)
