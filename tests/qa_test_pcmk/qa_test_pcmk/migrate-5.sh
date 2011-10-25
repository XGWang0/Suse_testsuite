#!/bin/bash


#Primitive migration with a clone
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-5 "Primitive migration with a clone"
test_results
clean_empty

