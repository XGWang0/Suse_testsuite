#!/bin/bash
#Ensure groups are migrated instead of remaining partially active on the current node
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-n-385265-2 "Ensure groups are migrated instead of remaining partially active on the current node"
test_results
clean_empty
