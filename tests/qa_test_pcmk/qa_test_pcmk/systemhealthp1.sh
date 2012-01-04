#!/bin/bash


#System Health (Progessive) 1
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealthp1 "System Health (Progessive)     1"
test_results
clean_empty

