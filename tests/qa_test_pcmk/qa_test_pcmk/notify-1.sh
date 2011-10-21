#!/bin/bash


#Notify simple
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test notify-1 "Notify simple"
test_results
clean_empty

