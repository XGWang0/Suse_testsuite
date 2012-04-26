#!/bin/bash
#Node Recover - Startup - no fence
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-1 "Node Recover - Startup   - no fence"
test_results
clean_empty
