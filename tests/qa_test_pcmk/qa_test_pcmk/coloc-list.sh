#!/bin/bash
#Colocation - many-to-one with list
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-list "Colocation - many-to-one with list"
test_results
clean_empty
