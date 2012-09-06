#!/bin/bash
#Stopped Monitor - initial stop
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-20	"Stopped Monitor - initial stop"
test_results
clean_empty
