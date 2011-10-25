#!/bin/bash


#No quorum - ignore
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test quorum-1 "No quorum - ignore"
test_results
clean_empty

