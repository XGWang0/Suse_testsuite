#!/bin/bash


#Redistribute clones with node-max > 1 and stickiness = 0
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2445 "Redistribute clones with node-max > 1 and stickiness = 0"
test_results
clean_empty

