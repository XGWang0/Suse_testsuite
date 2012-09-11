#!/bin/bash
#Prevent vm-01 from starting due to colocation/ordering
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-suse-707150 "Prevent vm-01 from starting due to colocation/ordering"
test_results
clean_empty
