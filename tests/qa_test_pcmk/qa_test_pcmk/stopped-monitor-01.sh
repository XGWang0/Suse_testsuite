#!/bin/bash
#Stopped Monitor - failed started
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-01	"Stopped Monitor - failed started"
test_results
clean_empty
