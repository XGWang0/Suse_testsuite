#!/bin/bash
#Node Recover - nothing active - fence 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-12 "Node Recover - nothing active - fence   "
test_results
clean_empty
