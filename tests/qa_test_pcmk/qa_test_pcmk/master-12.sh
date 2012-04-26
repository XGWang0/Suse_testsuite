#!/bin/bash
#Promotion based solely on rsc_location constraints
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-12 "Promotion based solely on rsc_location constraints"
test_results
clean_empty
