#./http3-server_rust --listen 127.0.0.1:6121 --key cert.key --cert cert.crt --root ./root/index.html --name www.example.org
#./http3-server 10.20.0.2 6121
RUST_LOG=debug ./http3-server_rust --listen 127.0.0.1:6121 --root ./root/index.html --cert cert.crt --key cert.key >> log_server
mv log_client log_client$(date +_%y%m%d-%H%M).out