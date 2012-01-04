#!/bin/bash


#Avoid needless restart of primitive depending on a clone
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2317 "Avoid needless restart of primitive depending on a clone"
test_results
clean_empty

