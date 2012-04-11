#!/bin/bash
#Group + Native 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group2 "Group + Native	"
test_results
clean_empty
