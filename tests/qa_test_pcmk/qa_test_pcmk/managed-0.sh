#!/bin/bash


#Managed (reference)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test managed-0 "Managed (reference)"
test_results
clean_empty

