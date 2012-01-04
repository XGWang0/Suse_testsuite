#!/bin/bash


#Schedule Monitor - move/pending start
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test mon-rsc-4 "Schedule Monitor - move/pending start"
test_results
clean_empty

