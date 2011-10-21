#!/bin/bash


#Notify move, confirm
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test notify-3 "Notify move, confirm"
test_results
clean_empty

