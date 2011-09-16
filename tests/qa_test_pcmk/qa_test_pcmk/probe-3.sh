#!/bin/bash
#Probe (pending node)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test probe-3 "Probe (pending node)"
test_results
clean_empty
