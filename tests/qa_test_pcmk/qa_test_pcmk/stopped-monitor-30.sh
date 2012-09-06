#!/bin/bash
#Stopped Monitor - new node started
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-30	"Stopped Monitor - new node started"
test_results
clean_empty
