#!/bin/bash
#Standby
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test standby "Standby"
test_results
clean_empty
