#!/bin/bash
#Params: Resource definition
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test params-2 "Params: Resource definition"
test_results
clean_empty
