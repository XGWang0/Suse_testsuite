#!/bin/bash


#string: eq (and) 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test attrs1 "string: eq (and)     "
test_results
clean_empty

