#!/bin/bash


#Order (move w/ restart) 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order6 "Order (move w/ restart)  "
test_results
clean_empty

