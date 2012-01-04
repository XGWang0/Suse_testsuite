#!/bin/bash


#Order (score=0) 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order-optional "Order (score=0)  "
test_results
clean_empty

