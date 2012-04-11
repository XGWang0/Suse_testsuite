#!/bin/bash
#Schedule Monitor - pending start 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test mon-rsc-3 "Schedule Monitor - pending start     "
test_results
clean_empty
