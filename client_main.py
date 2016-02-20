'''
The main function to start and run the client lives here!
'''

import sys
import protocols 

def main():
    protocol = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    p = Protocol(p)

    p.client_run(port)

    # read from console, run cmd (using p) 
    '''
    if cmd = get_messages:
        p.get_messages()
    '''
