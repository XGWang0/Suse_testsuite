#!/bin/bash


#Must (running) 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc_dep2  "Must (running) "
test_results
clean_empty

