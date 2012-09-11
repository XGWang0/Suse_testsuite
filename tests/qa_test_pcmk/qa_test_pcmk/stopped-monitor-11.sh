#!/bin/bash
#Stopped Monitor - stop unmanaged started
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-11	"Stopped Monitor - stop unmanaged started"
test_results
clean_empty
