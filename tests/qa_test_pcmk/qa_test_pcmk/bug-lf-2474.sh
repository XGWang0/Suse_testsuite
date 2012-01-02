#!/bin/bash


#Ensure resource op timeout takes precedence over op_defaults
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2474 "Ensure resource op timeout takes precedence over op_defaults"
test_results
clean_empty

