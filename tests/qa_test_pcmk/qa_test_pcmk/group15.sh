#!/bin/bash
#-ve group colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group15 "-ve group colocation"
test_results
clean_empty
