#!/bin/bash
#Dont promote partially active groups
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1822 "Dont promote partially active groups"
test_results
clean_empty
