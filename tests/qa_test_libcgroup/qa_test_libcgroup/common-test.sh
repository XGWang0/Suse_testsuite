#!/bin/bash

DATA_DIR="/usr/share/qa/qa_test_libcgroup"

cd $DATA_DIR/src/
make clean
make check
