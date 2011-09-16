#!/bin/bash
#Shutdown 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test simple7 "Shutdown    "
test_results
clean_empty
