#!/bin/bash
#Node Recover - HA down - fence 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-4 "Node Recover - HA down   - fence   "
test_results
clean_empty
