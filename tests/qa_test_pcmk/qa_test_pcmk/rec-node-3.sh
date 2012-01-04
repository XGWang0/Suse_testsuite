#!/bin/bash


#Node Recover - HA down - no fence
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-3 "Node Recover - HA down   - no fence"
test_results
clean_empty

