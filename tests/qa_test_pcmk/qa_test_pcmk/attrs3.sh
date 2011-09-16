#!/bin/bash
#string: ne (or) 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test attrs3 "string: ne (or)      "
test_results
clean_empty
