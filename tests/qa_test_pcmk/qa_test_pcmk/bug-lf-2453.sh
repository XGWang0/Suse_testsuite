#!/bin/bash
#Enforce mandatory clone ordering without colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2453 "Enforce mandatory clone ordering without colocation"
test_results
clean_empty
