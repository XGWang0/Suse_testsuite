#!/bin/bash


#Colocation with a specific clone instance (negative example)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-colocate-instance-1 "Colocation with a specific clone instance (negative example)"
test_results
clean_empty

