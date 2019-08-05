#./http3-client_rust --no-verify https://127.0.0.1:6121
#./http3-client_c 10.20.0.2 6121 > log_client
./http3-client_c 127.0.0.1 6121 |& tee log_client # "> log_client" to disable terminal output
mv log_client log_client$(date +_%y%m%d-%H%M).out