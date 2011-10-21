#!/bin/bash


#Resource Recover - stop - ignore
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-rsc-3 "Resource Recover - stop - ignore"
test_results
clean_empty

