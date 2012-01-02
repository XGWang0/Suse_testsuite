#!/bin/bash


#Stopped -> Promote
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-1 "Stopped -> Promote"
test_results
clean_empty

