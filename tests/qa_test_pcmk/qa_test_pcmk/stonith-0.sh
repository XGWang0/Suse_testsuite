#!/bin/bash


#Stonith loop - 1
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stonith-0 "Stonith loop - 1"
test_results
clean_empty

