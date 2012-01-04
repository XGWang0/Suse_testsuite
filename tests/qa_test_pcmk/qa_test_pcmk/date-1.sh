#!/bin/bash


#Dates
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test date-1 "Dates" -t "2005-020"
test_results
clean_empty

