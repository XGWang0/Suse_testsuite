#!/bin/bash


#System Health (Migrate On Red) 3
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealthm3 "System Health (Migrate On Red) 3"
test_results
clean_empty

