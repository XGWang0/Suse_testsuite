#!/bin/bash
#Stopped Monitor - failed stop
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-04	"Stopped Monitor - failed stop"
test_results
clean_empty
