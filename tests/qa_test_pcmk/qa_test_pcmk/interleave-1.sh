#!/bin/bash


#coloc - not interleaved
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test interleave-1 "coloc - not interleaved"
test_results
clean_empty

