'''
This script extracts the package sizes sent and received by the application.

Imports:
    - re (regular expressions) to extract packet sizes from output messages
    - sys to read command line arguments
'''

import re
import sys

received = []
sent = []
with open(sys.argv[1]) as f:
    for line in f:
        if 'sendmsg' in line:
            sent.append(line)
        elif 'recvmsg' in line:
            received.append(line)

regex = re.compile(r'= (\d+)$')

packets = []
for line in received:
    match = regex.search(line)
    if match:
        packets.append(int(match.group(1)))

print 'Received packet sizes: %s' % ', '.join(map(str, packets))
print 'Total received size: %s' % sum(packets)

packets = []
for line in sent:
    match = regex.search(line)
    if match:
        packets.append(int(match.group(1)))

print 'Sent packet sizes: %s' % ', '.join(map(str, packets))
print 'Total sent size: %s' % sum(packets)
