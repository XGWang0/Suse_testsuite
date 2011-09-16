#!/bin/bash
#is_dc: true 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test attrs6 "is_dc: true          "
test_results
clean_empty
