#!/bin/bash
#Stopped Monitor - unmanage started
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-09	"Stopped Monitor - unmanage started"
test_results
clean_empty
