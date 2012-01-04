#!/bin/bash


#Start Failed
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test simple4 "Start Failed"
test_results
clean_empty

