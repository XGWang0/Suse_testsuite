#!/bin/bash


#OSDL 1494 - Clone stability
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test 1494 "OSDL 1494 - Clone stability"
test_results
clean_empty

