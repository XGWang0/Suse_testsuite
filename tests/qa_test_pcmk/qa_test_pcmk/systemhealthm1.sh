#!/bin/bash
#System Health (Migrate On Red) 1
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealthm1 "System Health (Migrate On Red) 1"
test_results
clean_empty
