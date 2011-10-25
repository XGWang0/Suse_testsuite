#!/bin/bash


#Order (score=INFINITY) 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order-required "Order (score=INFINITY)  "
test_results
clean_empty

