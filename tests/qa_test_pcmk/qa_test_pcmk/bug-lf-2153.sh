#!/bin/bash
#Clone ordering constraints
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2153 "Clone ordering constraints"
test_results
clean_empty
