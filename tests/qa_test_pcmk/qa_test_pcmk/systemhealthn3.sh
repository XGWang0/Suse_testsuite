#!/bin/bash
#System Health (None) 3
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealthn3 "System Health (None)           3"
test_results
clean_empty
