#!/bin/bash


#Resource Recover - stop - fence 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-rsc-5 "Resource Recover - stop - fence "
test_results
clean_empty

