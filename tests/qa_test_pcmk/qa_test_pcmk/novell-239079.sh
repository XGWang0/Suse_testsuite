#!/bin/bash


#Notification priority
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test novell-239079 "Notification priority"
test_results
clean_empty

