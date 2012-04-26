#!/bin/bash
#Must 3 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc_dep7 "Must 3       "
test_results
clean_empty
