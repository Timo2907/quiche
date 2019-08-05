#!/bin/bash

cd ..
cargo build --examples
cd examples
mv ../target/debug/examples/http3-server ./http3-server_rust
mv ../target/debug/examples/http3-client ./http3-client_rust

