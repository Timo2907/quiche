#!/bin/bash

make clean; make
mv ./quic_server ./quic_server_c
mv ./quic_client ./quic_client_c
