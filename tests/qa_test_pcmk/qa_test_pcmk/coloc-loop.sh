#!/bin/bash


#Colocation - loop
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-loop "Colocation - loop"
test_results
clean_empty

