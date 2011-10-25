#!/bin/bash


#Stonith startup
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stonith-3 "Stonith startup"
test_results
clean_empty

