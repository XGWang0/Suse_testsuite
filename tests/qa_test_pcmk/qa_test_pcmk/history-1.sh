#!/bin/bash
#Correctly parse stateful-1 resource state
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test history-1 "Correctly parse stateful-1 resource state"
test_results
clean_empty
