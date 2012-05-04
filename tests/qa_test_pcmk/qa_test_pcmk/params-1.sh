#!/bin/bash
#Params: Changed
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test params-1 "Params: Changed"
test_results
clean_empty
