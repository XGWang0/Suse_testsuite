#!/bin/bash
#Not managed - down 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test managed-1 "Not managed - down "
test_results
clean_empty
