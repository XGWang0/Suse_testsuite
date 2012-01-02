#!/bin/bash


#Negative colocation with a group
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-negative-group "Negative colocation with a group"
test_results
clean_empty

