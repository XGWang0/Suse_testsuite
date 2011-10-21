#!/bin/bash


#Location constraint with multiple expressions
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bnc-515172 "Location constraint with multiple expressions"
test_results
clean_empty

