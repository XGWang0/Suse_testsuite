#!/bin/bash
#Date Spec - Pass
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test date-2 "Date Spec - Pass" -t "2005-020T12:30"
test_results
clean_empty
