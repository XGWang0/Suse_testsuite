#!/bin/bash


#Node Recover - no quorum - stop 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-9 "Node Recover - no quorum - stop    "
test_results
clean_empty

