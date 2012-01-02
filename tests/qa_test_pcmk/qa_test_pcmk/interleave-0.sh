#!/bin/bash


#Interleave (reference)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test interleave-0 "Interleave (reference)"
test_results
clean_empty

