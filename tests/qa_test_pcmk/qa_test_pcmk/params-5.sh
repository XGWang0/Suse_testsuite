#!/bin/bash
#Params: Restart based on probe digest
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test params-5 "Params: Restart based on probe digest"
test_results
clean_empty
