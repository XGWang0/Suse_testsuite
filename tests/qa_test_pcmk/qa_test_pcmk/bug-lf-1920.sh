#!/bin/bash


#Correctly handle probes that find active resources
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-1920 "Correctly handle probes that find active resources"
test_results
clean_empty

