#!/bin/bash


#Avoid clone shuffle
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2574 "Avoid clone shuffle"
test_results
clean_empty

