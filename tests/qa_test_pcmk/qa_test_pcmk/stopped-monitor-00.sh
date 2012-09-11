#!/bin/bash
#Stopped Monitor - initial start
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-00	"Stopped Monitor - initial start"
test_results
clean_empty
