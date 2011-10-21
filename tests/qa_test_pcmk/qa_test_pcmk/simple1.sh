#!/bin/bash


#Offline 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test simple1 "Offline     "
test_results
clean_empty

