#!/bin/bash


#System Health (Migrate On Red) 2
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealthm2 "System Health (Migrate On Red) 2"
test_results
clean_empty

