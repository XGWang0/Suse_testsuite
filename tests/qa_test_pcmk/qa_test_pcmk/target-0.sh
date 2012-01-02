#!/bin/bash


#Target Role : baseline
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test target-0 "Target Role : baseline"
test_results
clean_empty

