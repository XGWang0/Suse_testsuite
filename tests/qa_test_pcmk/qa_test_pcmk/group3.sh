#!/bin/bash


#Group + Group 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group3 "Group + Group	"
test_results
clean_empty

