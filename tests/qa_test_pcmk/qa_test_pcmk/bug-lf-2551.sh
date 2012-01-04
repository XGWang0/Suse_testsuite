#!/bin/bash


#STONITH ordering for stop
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2551 "STONITH ordering for stop"
test_results
clean_empty

