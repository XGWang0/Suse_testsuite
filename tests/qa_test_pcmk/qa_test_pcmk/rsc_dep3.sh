#!/bin/bash
#Must 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc_dep3 "Must         "
test_results
clean_empty
