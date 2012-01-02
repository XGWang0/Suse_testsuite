#!/bin/bash


#Promotion of cloned groups
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-group "Promotion of cloned groups"
test_results
clean_empty

