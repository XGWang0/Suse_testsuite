#!/bin/bash


#Utilization Order - Simple
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test utilization-order1 "Utilization Order - Simple"
test_results
clean_empty

