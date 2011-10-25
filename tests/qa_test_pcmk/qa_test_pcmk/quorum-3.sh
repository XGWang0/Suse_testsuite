#!/bin/bash


#No quorum - stop 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test quorum-3 "No quorum - stop  "
test_results
clean_empty

