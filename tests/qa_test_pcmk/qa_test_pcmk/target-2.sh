#!/bin/bash


#Target Role : invalid
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test target-2 "Target Role : invalid"
test_results
clean_empty

