#!/bin/bash


#Incarnation start order
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc1 "Incarnation start order"
test_results
clean_empty

