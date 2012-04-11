#!/bin/bash
#System Health (Only Green) 2
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealtho2 "System Health (Only Green)     2"
test_results
clean_empty
