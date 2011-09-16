#!/bin/bash
#Orphan ignore
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test orphan-0 "Orphan ignore"
test_results
clean_empty
