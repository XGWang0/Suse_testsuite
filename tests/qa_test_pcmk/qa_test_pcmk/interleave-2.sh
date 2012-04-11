#!/bin/bash
#coloc - interleaved 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test interleave-2 "coloc - interleaved   "
test_results
clean_empty
