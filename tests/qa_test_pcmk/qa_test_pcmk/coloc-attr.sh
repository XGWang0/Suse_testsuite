#!/bin/bash
#Colocation based on node attributes
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-attr "Colocation based on node attributes"
test_results
clean_empty
