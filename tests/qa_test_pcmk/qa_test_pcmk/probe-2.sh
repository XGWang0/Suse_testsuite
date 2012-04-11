#!/bin/bash
#Correctly re-probe cloned groups
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test probe-2 "Correctly re-probe cloned groups"
test_results
clean_empty
