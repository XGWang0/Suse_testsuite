#!/bin/bash
#System Health (Only Green) 1
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealtho1 "System Health (Only Green)     1"
test_results
clean_empty
