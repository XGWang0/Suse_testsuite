#!/bin/bash


#Non-migration in a group
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1820-1 "Non-migration in a group"
test_results
clean_empty

