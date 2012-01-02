#!/bin/bash


#Must not 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc_dep1 "Must not     "
test_results
clean_empty

