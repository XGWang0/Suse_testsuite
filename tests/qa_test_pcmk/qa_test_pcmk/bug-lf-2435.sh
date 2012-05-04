#!/bin/bash
#Colocation sets with a negative score
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2435 "Colocation sets with a negative score"
test_results
clean_empty
