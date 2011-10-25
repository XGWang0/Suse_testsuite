#!/bin/bash


#Ensure clones observe mandatory ordering constraints if the LHS is unrunnable
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2361 "Ensure clones observe mandatory ordering constraints if the LHS is unrunnable"
test_results
clean_empty

