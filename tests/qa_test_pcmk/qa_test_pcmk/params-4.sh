#!/bin/bash
#Params: Reload
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test params-4 "Params: Reload"
test_results
clean_empty
