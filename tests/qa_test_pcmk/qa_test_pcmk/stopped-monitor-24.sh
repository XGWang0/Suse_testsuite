#!/bin/bash
#Stopped Monitor - unmanage stopped
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-24	"Stopped Monitor - unmanage stopped"
test_results
clean_empty
