#!/bin/bash


#Stonith loop - 3
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stonith-2 "Stonith loop - 3"
test_results
clean_empty

