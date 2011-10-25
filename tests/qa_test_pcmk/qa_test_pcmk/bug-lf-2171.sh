#!/bin/bash


#Prevent group start when clone is stopped
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2171 "Prevent group start when clone is stopped"
test_results
clean_empty

