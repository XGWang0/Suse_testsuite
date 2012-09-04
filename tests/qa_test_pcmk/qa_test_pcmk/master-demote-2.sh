#!/bin/bash
#Demote does not clear past failure
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-demote-2 "Demote does not clear past failure"
test_results
clean_empty
