#!/bin/bash


#Mandatory group ordering - Stop group_FUN
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1718 "Mandatory group ordering - Stop group_FUN"
test_results
clean_empty

