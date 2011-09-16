#!/bin/bash
#Utilization Order - Migrate
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test utilization-order3 "Utilization Order - Migrate"
test_results
clean_empty
