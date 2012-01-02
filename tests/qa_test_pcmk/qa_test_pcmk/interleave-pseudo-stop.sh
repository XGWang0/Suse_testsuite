#!/bin/bash


#Interleaved clone during stonith
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test interleave-pseudo-stop "Interleaved clone during stonith"
test_results
clean_empty

