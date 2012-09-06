#!/bin/bash
#Stopped Monitor - unmanaged started multi-up
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-10	"Stopped Monitor - unmanaged started multi-up"
test_results
clean_empty
