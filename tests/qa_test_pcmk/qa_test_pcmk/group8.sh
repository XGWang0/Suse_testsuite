#!/bin/bash
#Group anti-colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group8 "Group anti-colocation"
test_results
clean_empty
