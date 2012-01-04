#!/bin/bash


#Mandatory master colocation constraints
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-promotion-constraint "Mandatory master colocation constraints"
test_results
clean_empty

