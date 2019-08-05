#!/bin/bash

cd ..
cargo build --examples
cd examples
mv ../target/debug/examples/server ./server_rust
mv ../target/debug/examples/client ./client_rust

