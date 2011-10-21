#!/bin/bash


#Priority (eq)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test simple12 "Priority (eq)"
test_results
clean_empty

