'''
The main function to start and run the client lives here!
'''

import sys
import os
import curses
import curses.textpad
import thread
import time

from protobuf.protobuf_wrapper import Protobuf_Protocol
from collections import defaultdict
from frontend.application import Application


def main(screen):
    protocol = sys.argv[1]
    port = sys.argv[2]
    if protocol == 'protobuf':
        p = Protobuf_Protocol(int(port))

    window = Application(screen, p)
    window.run()    

if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main)
