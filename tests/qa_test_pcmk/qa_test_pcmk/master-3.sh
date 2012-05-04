#!/bin/bash
#Stopped -> Promote : master location
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-3 "Stopped -> Promote : master location"
test_results
clean_empty
