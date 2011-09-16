#!/bin/bash
#Include preferences of colocated resources when placing master
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-13 "Include preferences of colocated resources when placing master"
test_results
clean_empty
