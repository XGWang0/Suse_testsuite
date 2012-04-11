#!/bin/bash
#Promoted -> Fenced
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-7 "Promoted -> Fenced"
test_results
clean_empty
