#!/bin/bash


#Orphan processing with clone-max=0
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-max-zero "Orphan processing with clone-max=0"
test_results
clean_empty

