#!/bin/bash


#Resource Recover - monitor 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-rsc-2 "Resource Recover - monitor      "
test_results
clean_empty

