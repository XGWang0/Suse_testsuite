#!/bin/bash
#Node Recover - Startup - fence 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-2 "Node Recover - Startup   - fence   "
test_results
clean_empty
