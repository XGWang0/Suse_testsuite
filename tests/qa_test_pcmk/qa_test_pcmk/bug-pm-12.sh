#!/bin/bash
#Recover only the failed portion of a cloned group
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-pm-12 "Recover only the failed portion of a cloned group"
test_results
clean_empty
