#!/bin/bash


#Optimized Placement Strategy - priority
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test placement-priority   "Optimized Placement Strategy - priority"
test_results
clean_empty

