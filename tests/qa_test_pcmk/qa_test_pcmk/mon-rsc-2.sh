#!/bin/bash
#Schedule Monitor - move 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test mon-rsc-2 "Schedule Monitor - move "
test_results
clean_empty
