#!/bin/bash


#Resource Recover - multiple - stop 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-rsc-7 "Resource Recover - multiple - stop   "
test_results
clean_empty

