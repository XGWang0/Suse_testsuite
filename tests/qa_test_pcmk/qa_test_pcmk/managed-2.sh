#!/bin/bash


#Not managed - up 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test managed-2 "Not managed - up   "
test_results
clean_empty

