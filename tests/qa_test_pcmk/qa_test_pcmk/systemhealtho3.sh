#!/bin/bash


#System Health (Only Green) 3
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealtho3 "System Health (Only Green)     3"
test_results
clean_empty

