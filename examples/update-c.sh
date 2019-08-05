#!/bin/bash

make clean; make
mv ./http3-server ./http3-server_c
mv ./http3-client ./http3-client_c
