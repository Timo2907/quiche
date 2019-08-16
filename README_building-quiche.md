### QUICHE install on Ubuntu Server
0. Install dependencies
	0.1 sudo apt-get install libunwind-dev
	0.2 sudo apt-get install golang
	0.3 sudo apt-get install libev-dev
	0.4 uthash
	
1. Install RUST programming language
	1.1 curl -sf -L https://static.rust-lang.org/rustup.sh | sh
	1.2 source $HOME/.cargo/env
	1.3 rustc --version
	
2. Checkout QUICHE code and build the binaries
	2.1 git clone https://github.com/Timo2907/quiche
	2.2 git submodule update --init
	2.3 quiche/example/update-rust.sh
	2.4 quiche/example/update-c.sh
	2.5 cargo test

3. Run examples
	3.1 quiche/examples/start_quiche_server.sh
	3.2 quiche/examples/start_quiche_client.sh
	
------------------------------------------

3. Test QUICHE http3-client and http3-server
	3.1 ./http3-client quic.tech 8443
		=> connections to the QUICHE test server

	3.2 ./http3-server 127.0.0.1 6121
	3.3 ./http3-client 127.0.0.1 6121
		=> Client connects to server and downloads SOMETHING (-> is there a default root in the .c server? 
																	-> change it to the www.example.org-directory and run make again for new erver binary for tests)

NOTE: Rust BUILD FILES are in "target/debug/example" (!)
	3.1 ./http3-server_rust --listen 127.0.0.1:6121 --key cert.key --cert cert.crt --root ./root/index.html --name www.example.org
		./server_rust --listen 127.0.0.1:6121 --key cert.key --cert cert.crt --root ./root/index.html --name www.example.org
			=> sets up server (but server does not give output when C client connects with " http3-client_c www.example.org " ?)
	
		./http3-client_rust [--no-verify] https://quic.tech:8443
			=> Not Found!
			
		./http3-client_rust [--no-verify] http://[www.]example.org:6121
			=> no output
			
		./http3-client_rust https://127.0.0.1:6121  
			=> recv failed: TlsFail
		./http3-client_rust --no-verify https://127.0.0.1:6121
			(=> Not Found! -> SERVER ROOT WAS WRONG!)

-------------------------------------------------

4. WORKING WITH QUICHE:
	4.0 syncing Windows directory with MAKI directory
		4.0.1 Open Cygwin Terminal
		4.0.2 rsync -avzhe ssh --progress --exclude examples/build /cygdrive/c/Users/Timo/Documents/TU-Darmstadt/Master-4-Semester/Masterthesis/Code/quiche/ maki@10.0.30.15:/home/maki/quiche

	4.1 RUST
		- compiling files with quiche/examples/update-rust.sh
		- to get the output, set environment variable to... e.g. "RUST_LOG=trace" or "RUST_LOG=debug"
		
	4.2 C
		- compiling files with quiche/examples/update-c.sh
		- ./http3-client 127.0.0.1 6121
		- http3-client_c: change output from stderr to stdout for logging (22x)

	
