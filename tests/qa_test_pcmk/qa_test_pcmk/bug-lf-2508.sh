#!/bin/bash
#Correctly reconstruct the status of anonymous cloned groups
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2508 "Correctly reconstruct the status of anonymous cloned groups"
test_results
clean_empty
