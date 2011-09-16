#!/bin/bash
#Promoted -> Fenced -> Moved
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-8 "Promoted -> Fenced -> Moved"
test_results
clean_empty
