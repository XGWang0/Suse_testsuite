#!/bin/bash


#Intra-set colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-intra-set "Intra-set colocation"
test_results
clean_empty

