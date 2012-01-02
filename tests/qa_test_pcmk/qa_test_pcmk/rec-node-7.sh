#!/bin/bash


#Node Recover - no quorum - ignore 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-7 "Node Recover - no quorum - ignore  "
test_results
clean_empty

