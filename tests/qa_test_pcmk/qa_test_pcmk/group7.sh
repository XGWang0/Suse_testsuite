#!/bin/bash
#Group colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group7 "Group colocation"
test_results
clean_empty
