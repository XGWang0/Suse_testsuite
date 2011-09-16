#!/bin/bash
#Interleaved clone during dependancy restart
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test interleave-restart "Interleaved clone during dependancy restart"
test_results
clean_empty
