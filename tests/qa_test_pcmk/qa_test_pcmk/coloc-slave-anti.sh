#!/bin/bash


#Anti-colocation with slave shouldn't prevent master colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-slave-anti "Anti-colocation with slave shouldn't prevent master colocation"
test_results
clean_empty

