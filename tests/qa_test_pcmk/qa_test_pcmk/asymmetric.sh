#!/bin/bash


#Asymmetric - require explicit location constraints
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test asymmetric "Asymmetric - require explicit location constraints"
test_results
clean_empty

