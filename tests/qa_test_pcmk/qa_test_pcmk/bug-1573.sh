#!/bin/bash
#Partial stop of a group with two children
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1573 "Partial stop of a group with two children"
test_results
clean_empty
