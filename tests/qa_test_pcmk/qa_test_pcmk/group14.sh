#!/bin/bash


#Group stop (graph terminated)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group14 "Group stop (graph terminated)"
test_results
clean_empty

