#!/bin/bash
#System Health () 1
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test systemhealth1  "System Health ()               1"
test_results
clean_empty
