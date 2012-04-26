#!/bin/bash
#is_dc: false 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test attrs7 "is_dc: false         "
test_results
clean_empty
