#!/bin/bash
#System Health (None) 1
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealthn1 "System Health (None)           1"
test_results
clean_empty
