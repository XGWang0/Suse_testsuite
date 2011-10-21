#!/bin/bash


#New resource added to a m/s group
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-pm-11 "New resource added to a m/s group"
test_results
clean_empty

