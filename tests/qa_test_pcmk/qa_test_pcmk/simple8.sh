#!/bin/bash


#Stickiness
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test simple8 "Stickiness"
test_results
clean_empty

