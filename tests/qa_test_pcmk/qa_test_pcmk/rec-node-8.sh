#!/bin/bash


#Node Recover - no quorum - freeze 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-8 "Node Recover - no quorum - freeze  "
test_results
clean_empty

