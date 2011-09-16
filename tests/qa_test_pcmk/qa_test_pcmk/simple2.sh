#!/bin/bash
#Start 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test simple2 "Start       "
test_results
clean_empty
