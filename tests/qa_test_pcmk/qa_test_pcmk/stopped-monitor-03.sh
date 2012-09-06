#!/bin/bash
#Stopped Monitor - stop started
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-03	"Stopped Monitor - stop started"
test_results
clean_empty
