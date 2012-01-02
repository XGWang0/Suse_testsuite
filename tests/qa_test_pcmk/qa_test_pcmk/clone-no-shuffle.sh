#!/bin/bash


#Dont prioritize allocation of instances that must be moved
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-no-shuffle "Dont prioritize allocation of instances that must be moved"
test_results
clean_empty

