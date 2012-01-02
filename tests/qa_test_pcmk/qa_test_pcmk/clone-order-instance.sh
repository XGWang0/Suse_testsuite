#!/bin/bash


#Ordering with specific clone instances
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-order-instance "Ordering with specific clone instances"
test_results
clean_empty

