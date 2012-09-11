#!/bin/bash
#Stonith implies demote
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2606 "Stonith implies demote"
test_results
clean_empty
