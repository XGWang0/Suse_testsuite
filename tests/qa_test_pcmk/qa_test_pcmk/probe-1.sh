#!/bin/bash


#Pending Probe
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test probe-1 "Pending Probe"
test_results
clean_empty

