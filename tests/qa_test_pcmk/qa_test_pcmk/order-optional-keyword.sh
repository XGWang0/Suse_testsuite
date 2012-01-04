#!/bin/bash


#Order (optional keyword)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order-optional-keyword "Order (optional keyword)"
test_results
clean_empty

