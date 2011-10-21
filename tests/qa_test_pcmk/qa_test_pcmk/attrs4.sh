#!/bin/bash


#string: exists 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test attrs4 "string: exists       "
test_results
clean_empty

