#!/bin/bash
#Orphan stop
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test orphan-1 "Orphan stop"
test_results
clean_empty
