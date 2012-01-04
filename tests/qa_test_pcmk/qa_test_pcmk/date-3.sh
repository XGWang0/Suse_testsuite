#!/bin/bash


#Date Spec - Fail
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test date-3 "Date Spec - Fail" -t "2005-020T11:30"
test_results
clean_empty

