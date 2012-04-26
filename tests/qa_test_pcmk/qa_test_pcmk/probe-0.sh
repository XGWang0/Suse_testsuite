#!/bin/bash
#Probe (anon clone)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test probe-0 "Probe (anon clone)"
test_results
clean_empty
