#!/bin/bash
#Colocation - many-to-one
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-many-one "Colocation - many-to-one"
test_results
clean_empty
