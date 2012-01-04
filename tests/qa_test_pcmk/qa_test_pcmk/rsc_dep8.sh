#!/bin/bash


#Must (running : alt) 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc_dep8  "Must (running : alt) "
test_results
clean_empty

