#!/bin/bash


#Clone shutdown
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc12 "Clone shutdown"
test_results
clean_empty

