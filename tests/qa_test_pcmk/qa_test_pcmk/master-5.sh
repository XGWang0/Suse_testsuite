#!/bin/bash


#Promoted -> Promoted
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-5 "Promoted -> Promoted"
test_results
clean_empty

