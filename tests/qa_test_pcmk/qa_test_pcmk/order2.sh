#!/bin/bash
#Order start 2 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order2 "Order start 2     "
test_results
clean_empty
