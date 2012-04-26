#!/bin/bash
#Stopped -> Promotable : notify with monitor
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-10 "Stopped -> Promotable : notify with monitor"
test_results
clean_empty
