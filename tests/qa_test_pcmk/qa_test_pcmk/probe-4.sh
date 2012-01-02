#!/bin/bash


#Probe (pending node + stopped resource)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test probe-4 "Probe (pending node + stopped resource)" --rc 4
test_results
clean_empty

