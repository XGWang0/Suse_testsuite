#!/bin/bash


#Depends-on-master ordering
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1685 "Depends-on-master ordering"
test_results
clean_empty

