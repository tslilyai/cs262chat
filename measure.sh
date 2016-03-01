echo "testing protocol $1"
python server_main.py --port 12353 --protocol $1 > log1.txt 2>&1 &
SERVER_PID=$!
sudo strace -p $SERVER_PID -f -e trace=network -s 10000 > netcalls.txt 2>&1 &
sleep 1
python client_main.py --port 12353 --protocol $1 < transcript.txt &
CLIENT_PID=$!
sleep 3
kill $CLIENT_PID
sleep 1
kill -KILL $CLIENT_PID
kill -KILL $SERVER_PID

echo "======================================================"
python analyze.py netcalls.txt
