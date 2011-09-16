#!/bin/bash
#Balanced clone placement
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2544 "Balanced clone placement"
test_results
clean_empty
