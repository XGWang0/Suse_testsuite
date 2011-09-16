#!/bin/bash
#Order stop 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order3 "Order stop	  "
test_results
clean_empty
