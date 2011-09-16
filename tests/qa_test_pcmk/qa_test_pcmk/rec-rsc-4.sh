#!/bin/bash
#Resource Recover - stop - block 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-rsc-4 "Resource Recover - stop - block "
test_results
clean_empty
