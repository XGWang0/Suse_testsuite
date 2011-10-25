#!/bin/bash


#Resource Recover - no start 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-rsc-0 "Resource Recover - no start     "
test_results
clean_empty

