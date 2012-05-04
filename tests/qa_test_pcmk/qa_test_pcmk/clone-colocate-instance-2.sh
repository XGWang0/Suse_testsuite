#!/bin/bash
#Colocation with a specific clone instance
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-colocate-instance-2 "Colocation with a specific clone instance"
test_results
clean_empty
