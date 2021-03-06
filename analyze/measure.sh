# This script executes the commands in transcript.txt within the chat application 
# and records the calls over the network made by the client.
#
# network.txt and log1.txt can then be passed to analyze.py to extract packet sizes

echo "testing protocol $1"
python ../server_main.py --port 12353 --protocol $1 > log1.txt 2>&1 &
SERVER_PID=$!
sudo strace -p $SERVER_PID -f -e trace=network -s 10000 > netcalls.txt 2>&1 &
sleep 1 # Make sure the server is ready before starting client
python ../client_main.py --port 12353 --protocol $1 < transcript.txt &
CLIENT_PID=$!
sleep 3 # Give client a chance to finish all the messages
kill $CLIENT_PID
sleep 1 # Give client a chance to terminate communications cleanly (restore curses environment, etc)
kill -KILL $CLIENT_PID # Now hard kill both client and server
kill -KILL $SERVER_PID

echo "======================================================"
python analyze.py netcalls.txt
