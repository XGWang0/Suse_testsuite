#!/bin/bash
#Restart all anonymous clone instances after config change
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2106 "Restart all anonymous clone instances after config change"
test_results
clean_empty
