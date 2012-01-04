#!/bin/bash


#string: not_exists 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test attrs5 "string: not_exists   "
test_results
clean_empty

