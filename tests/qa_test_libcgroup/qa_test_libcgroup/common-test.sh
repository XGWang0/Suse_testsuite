#!/bin/bash

DATA_DIR="/usr/share/qa/qa_test_libcgroup"

cd $DATA_DIR/src/
./config.status
make clean
make check
