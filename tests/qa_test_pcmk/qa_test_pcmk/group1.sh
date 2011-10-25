#!/bin/bash


#Group 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group1 "Group		"
test_results
clean_empty

