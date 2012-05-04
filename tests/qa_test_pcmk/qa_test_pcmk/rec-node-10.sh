#!/bin/bash
#Node Recover - no quorum - stop w/fence
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-10 "Node Recover - no quorum - stop w/fence"
test_results
clean_empty
