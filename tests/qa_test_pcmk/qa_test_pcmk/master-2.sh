#!/bin/bash
#Stopped -> Promote : notify
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-2 "Stopped -> Promote : notify"
test_results
clean_empty
