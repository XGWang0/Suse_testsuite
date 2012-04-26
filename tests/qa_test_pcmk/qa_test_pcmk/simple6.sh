#!/bin/bash
#Stop Start 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test simple6 "Stop Start  "
test_results
clean_empty
