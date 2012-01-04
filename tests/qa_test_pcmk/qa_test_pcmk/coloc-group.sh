#!/bin/bash


#Colocation - groups
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-group "Colocation - groups"
test_results
clean_empty

