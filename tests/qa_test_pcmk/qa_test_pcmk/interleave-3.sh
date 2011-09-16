#!/bin/bash
#coloc - interleaved (2)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test interleave-3 "coloc - interleaved (2)"
test_results
clean_empty
