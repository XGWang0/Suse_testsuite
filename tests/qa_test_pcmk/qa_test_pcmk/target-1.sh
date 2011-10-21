#!/bin/bash


#Target Role : master
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test target-1 "Target Role : master"
test_results
clean_empty

