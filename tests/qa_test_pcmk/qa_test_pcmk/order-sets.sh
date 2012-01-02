#!/bin/bash


#Ordering for resource sets
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order-sets "Ordering for resource sets"
test_results
clean_empty

