#!/bin/bash


#Migration in a group
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1820 "Migration in a group"
test_results
clean_empty

