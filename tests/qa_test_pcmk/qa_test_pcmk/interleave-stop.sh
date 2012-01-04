#!/bin/bash


#Interleaved clone during stop
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test interleave-stop "Interleaved clone during stop"
test_results
clean_empty

