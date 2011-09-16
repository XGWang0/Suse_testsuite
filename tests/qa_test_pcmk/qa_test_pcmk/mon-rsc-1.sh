#!/bin/bash
#Schedule Monitor - start
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test mon-rsc-1 "Schedule Monitor - start"
test_results
clean_empty
