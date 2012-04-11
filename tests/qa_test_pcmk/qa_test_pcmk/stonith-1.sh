#!/bin/bash
#Stonith loop - 2
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stonith-1 "Stonith loop - 2"
test_results
clean_empty
