#!/bin/bash
#Order (multiple) 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order4 "Order (multiple)  "
test_results
clean_empty
