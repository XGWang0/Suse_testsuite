#!/bin/bash


#score_attribute 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test attrs8 "score_attribute      "
test_results
clean_empty

