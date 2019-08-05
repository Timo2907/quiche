#./http3-client_rust --no-verify https://127.0.0.1:6121
#./http3-client_c 10.20.0.2 6121 > log_client
./http3-client_c 127.0.0.1 6121 > log_client1
./http3-client_c 127.0.0.1 6121 > log_client2
./http3-client_c 127.0.0.1 6121 > log_client3
mv log_client1 log_client1$(date +_%y%m%d-%H%M).out
mv log_client2 log_client2$(date +_%y%m%d-%H%M).out
mv log_client3 log_client3$(date +_%y%m%d-%H%M).out