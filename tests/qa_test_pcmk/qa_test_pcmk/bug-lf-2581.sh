#!/bin/bash
#Avoid group restart due to unrelated clone (re)start
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2581 "Avoid group restart due to unrelated clone (re)start"
test_results
clean_empty
