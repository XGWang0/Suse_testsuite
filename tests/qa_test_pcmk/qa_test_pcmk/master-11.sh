#!/bin/bash
#Stopped -> Promote : colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-11 "Stopped -> Promote : colocation"
test_results
clean_empty
