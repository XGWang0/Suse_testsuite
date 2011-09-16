#!/bin/bash
#Must not 3 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc_dep5 "Must not 3   "
test_results
clean_empty
