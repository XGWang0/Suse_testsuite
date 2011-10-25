#!/bin/bash


#Utilization Order - Complex
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test utilization-order2 "Utilization Order - Complex"
test_results
clean_empty

